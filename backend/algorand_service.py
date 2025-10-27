import algod
from algosdk import account, transaction, mnemonic
from algosdk.atomic_transaction_composer import AtomicTransactionComposer
from algosdk.future.transaction import ApplicationNoOpTxn, AssetTransferTxn
from pyteal import compileTeal, Mode
from fastapi import FastAPI

# Connect to TestNet (replace with MainNet for prod)
algod_client = algod.AlgodClient("your_token", "https://testnet-api.algonode.cloud")

# Generate or use accounts
employer_sk = mnemonic.to_private_key("your_employer_mnemonic")
employer_addr = account.address_from_private_key(employer_sk)
worker_addr = "WORKER_ACCOUNT_ADDRESS"  # From frontend wallet

# Create ASA for wages (if not exists)
def create_wage_asa():
    params = algod_client.suggested_params()
    txn = transaction.AssetConfigTxn(
        sender=employer_addr,
        sp=params,
        total=1000000,  # Total supply
        decimals=2,
        default_frozen=False,
        unit_name="WAGE",
        asset_name="StreamWage",
        manager=employer_addr,
        reserve=employer_addr,
        freeze=employer_addr,
        clawback=employer_addr,
        url="https://your-dapp-url.com"
    )
    signed_txn = txn.sign(employer_sk)
    tx_id = algod_client.send_transaction(signed_txn)
    return algod_client.pending_transaction_info(tx_id)['asset-index']

# Deploy contract
def deploy_contract():
    from contracts.streaming_wage import approval_program, clear_program  # Import from your contracts
    approval_bytes = compileTeal(approval_program(), Mode.Application, version=6, assembleConstants=True)
    clear_bytes = compileTeal(clear_program(), Mode.Application, version=6, assembleConstants=True)

    params = algod_client.suggested_params()
    txn1 = transaction.ApplicationCreateTxn(
        sender=employer_addr,
        sp=params,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_bytes,
        clear_program=clear_bytes,
        global_schema=transaction.StateSchema(num_uints=3, num_byte_slices=0),
        local_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
        app_args=["1000", "0"]  # wage_rate=1 ALGO/hour, initial_hours=0
    )
    signed_txn = txn1.sign(employer_sk)
    tx_id = algod_client.send_transaction(signed_txn)
    result = algod_client.pending_transaction_info(tx_id)
    app_id = result['application-index']
    return app_id

# Stream wages (call from API endpoint)
def stream_wages(app_id, hours_worked):
    params = algod_client.suggested_params()
    atc = AtomicTransactionComposer()
    atc.add_method_call(app_id, employer_addr, params, employer_sk,
                        sp=algod_client.suggested_params(),
                        method_args=["update_hours", str(hours_worked)],
                        accounts=[worker_addr],
                        foreign_assets=[create_wage_asa()])  # Opt-in worker to ASA first
    signed_txn = atc.assemble_and_sign_transactions()
    tx_id = algod_client.send_transactions(signed_txn)
    return algod_client.pending_transaction_info(tx_id)

# Example usage in your FastAPI endpoint
app = FastAPI()

@app.post("/disburse_wage")
def disburse(hours: int):
    app_id = deploy_contract() if not globals().get('app_id') else globals()['app_id']
    result = stream_wages(app_id, hours)
    return {"tx_id": result['txn']['txid'], "status": "Wage streamed"}

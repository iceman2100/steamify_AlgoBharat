from pyteal import *

def approval_program():
    # Global state: wage_rate (microAlgos per hour), total_hours_worked, employer_account
    on_create = Seq([
        App.globalPut(Int(0), Btoi(Txn.application_args[0])),  # wage_rate
        App.globalPut(Int(1), Btoi(Txn.application_args[1])),  # initial total_hours
        App.globalPut(Int(2), Txn.sender),  # employer
        Return(Int(1))
    ])

    is_employer = App.globalGet(Int(2)) == Txn.sender
    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, Seq([
            Assert(is_employer),
            Assert(Txn.application_args.length() == Int(2)),
            # Update hours worked and calculate payout
            If(Txn.application_args[0] == Bytes("update_hours"),
                App.globalPut(Int(1), App.globalGet(Int(1)) + Btoi(Txn.application_args[1]))
            ),
            # Stream wage: inner transaction for ASA transfer
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Int(12345678),  # Your wage ASA ID
                TxnField.asset_amount: App.globalGet(Int(0)) * App.globalGet(Int(1)),  # rate * hours
                TxnField.asset_receiver: Txn.accounts[1],  # worker account
            }),
            InnerTxnBuilder.Submit(),
            Return(Int(1))
        ])],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Int(1))]
    )
    return compileTeal(program, Mode.Application, version=6)

def clear_program():
    program = Seq([
        # Optional: Transfer remaining funds to employer
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: App.globalGet(Int(0)),  # Remaining balance
            TxnField.receiver: App.globalGet(Int(2)),
        }),
        InnerTxnBuilder.Submit(),
        Return(Int(1))
    ])
    return compileTeal(program, Mode.Application, version=6)

if __name__ == "__main__":
    with open("streaming_wage_approval.teal", "w") as f:
        f.write(compileTeal(approval_program(), Mode.Application, version=6))
    with open("streaming_wage_clear.teal", "w") as f:
        f.write(compileTeal(clear_program(), Mode.Application, version=6))

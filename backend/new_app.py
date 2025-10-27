from flask import Flask, jsonify, request
from datetime import datetime
from web3 import Web3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to Sepolia testnet
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/a85f2c76df734dfaaad5516c2cf513a4'))

# Contract addresses
STREAM_FI_ADDRESS = '0x9A9f2CCfdE556A7E9Ff0848998Aa4a0CFD8863AE'
TOKEN_ADDRESS = '0x68B1D87F95878fE05B998F19b66F4baba5De1aed'

# ABIs
STREAM_FI_ABI = [
    {
        "inputs": [{"name": "address", "type": "address"}],
        "name": "streams",
        "outputs": [
            {"name": "sender", "type": "address"},
            {"name": "recipient", "type": "address"},
            {"name": "startTime", "type": "uint256"},
            {"name": "ratePerSecond", "type": "uint256"},
            {"name": "lastClaimTime", "type": "uint256"},
            {"name": "isActive", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

TOKEN_ABI = [
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Initialize contracts
stream_fi = w3.eth.contract(address=STREAM_FI_ADDRESS, abi=STREAM_FI_ABI)
token = w3.eth.contract(address=TOKEN_ADDRESS, abi=TOKEN_ABI)

@app.route('/stream/<address>')
def get_stream(address):
    try:
        stream = stream_fi.functions.streams(address).call()
        balance = token.functions.balanceOf(address).call()
        
        return jsonify({
            'address': address,
            'balance': Web3.fromWei(balance, 'ether'),
            'stream_rate': Web3.fromWei(stream[3], 'ether'),
            'is_active': stream[5],
            'last_claim': datetime.fromtimestamp(stream[4]).isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/metrics')
def get_metrics():
    try:
        total_supply = token.functions.totalSupply().call()
        return jsonify({
            'total_supply': Web3.fromWei(total_supply, 'ether'),
            'network': 'Sepolia',
            'chain_id': 11155111
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, jsonify, request
import blockchain as bc
import json
import block
import time
import sys

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = bc.Blockchain()

@app.route('/register/node', methods=['POST']):
def register_node():
    pass

@app.reoute('/chain/consensus')
def consesus():
    pass

@app.route('/chain/checkValidity')
def check_chain_validity():
    pass

@app.route('/chain')
def index():
    
    chain = blockchain.chain
    json_chain = []
    
    for block in chain:
        json_chain.append(block.toJson())
        
    data = {
        'chain': json_chain,
        'chain_length': len(json_chain)
    }
    
    return jsonify(data)

@app.route('/transaction/new', methods=['POST'])
def makeTransaction():
    values = request.get_json()
    
    required = ["sender", "receiver", "amount"]
    

    """
    transaction = {
        'sender': values['sender'],
        'receiver': values['receiver'],
        'amount': values['amount'],
    }
    """
    transaction = {
        'sender': "ilias",
        'receiver': "Seulgi",
        'amount': "10",
    }
    
    blockchain.new_transaction(transaction)
    
    response = "Transaction will be added"
    
    return jsonify(response), 200
    
@app.route('/mine')
def mine():
    if  len(blockchain.unconfirmedBlocks) == 0:
        return "No block to mine", 400
    
    pending_transaction = blockchain.unconfirmedBlocks[0]
    blockCreated = block.Block(len(blockchain.chain), pending_transaction, blockchain.chain[-1].hash, time.time())
    blockHash = blockchain.proofOfWork(blockCreated)
    done = blockchain.add_block(blockCreated, blockHash)
    
    if done:
        response = "Block {0} mined".format(blockCreated.index)
        blockchain.unconfirmedBlocks.remove(pending_transaction)
        return jsonify(response)
    else:
        return "Error while mining block", 400

@app.route('/transaction/pending')
def pending_transaction():
    pending = blockchain.unconfirmedBlocks
    
    return jsonify(pending)
    

if __name__ == "__main__":
    args = sys.argv
    port = args[1]
    app.run(debug=True, port=port)
    
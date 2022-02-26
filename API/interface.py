from flask import Flask, jsonify, request
import json
import time
import sys
import requests
from colorama import Fore

from BC import utils as ut
from BC import block as block
from BC import blockchain as bc

from wallet import wallet_adrs

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = bc.Blockchain()

adresse_to_sync_with = "http://127.0.0.1:50/" # we suppose that this adresse is always on for the moment

def main():
    if len(sys.argv) > 1:
        print(Fore.GREEN+"Launching server :"+Fore.WHITE)
        port = sys.argv[1]
        app.run(debug=True, port=port)
    else:
        app.run(debug=True)


@app.route('/create/wallet')
def create_wallet():
    wallet = wallet_adrs.wallet()

    to_return = {
        "pk" : wallet.get_privateKey().decode(),
        "pubk" : wallet.get_publicKey().decode(),
        "adress" : wallet.get_address().decode()
    }

    return jsonify(to_return)

@app.route('/register/node/create/adresse')
def create_adresse():
    return jsonify(ut.adresse_gen(blockchain.nodes))

@app.route('/register/node', methods=['POST'])
def register_node():
    required = ["adresse", "url"]
    
    value = request.form

    for req in required:
        if req not in value:
            return "Cannot register node, please proceed with an adresse and url", 400

    if not ut.adress_checkVadility_Avaibality(value["adresse"], blockchain.nodes):
        return "Can't use {0} this as an adresse".format(value["adresse"]), 400

    for node in blockchain.nodes:
        if node["url"] == value["url"]:
            return "Can't use this as an url already used"
    
    if value["adresse"] in blockchain.nodes:
        return "Adresse already listed in the nodes", 400

    blockchain.add_node(value["adresse"], value["url"])
    
    response = "{0} added to the node.".format(value["adresse"])
    
    # TODO : tell all the nodes to add this node too
    
    return response, 200

@app.route('/chain/consensus')
def consesus():
    chain_after_consensus = blockchain.consensus()
    return jsonify(chain_after_consensus)

@app.route('/chain/nodes')
def getNodes():
    nodes = blockchain.nodes
    
    return jsonify(nodes), 200

@app.route('/chain/checkValidity')
def check_chain_validity():
    valid = blockchain.checkChain()

    if valid:
        return "The chain is valid", 200
    
    return "The chain is not valid, proceed concensus"; 400
    
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
    values = request.form
        
    required = ["sender", "receiver", "amount"]
    
    for req in required:
        if not req in values:
            return "Missing arguments", 400
    
    if values['sender'] ==  values['receiver']:
        return "Cannot make transaction with the same sender and receiver", 200

    receiver_exist = False
    sender_exist = False
    for node in blockchain.nodes:
        if not receiver_exist:
           if values["receiver"] == node["adresse"]:
               receiver_exist = True
        if not sender_exist:
           if values["sender"] == node["adresse"]:
               sender_exist = True
    
    if receiver_exist and sender_exist:
        transaction = {
            'sender': values['sender'],
            'receiver': values['receiver'],
            'amount': values['amount']
        }
        blockchain.new_transaction(transaction)
        response = "Transaction will be added"
        return jsonify(response), 200

    return "Cannot make transaction, adresses do not exists"
    
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

@app.route('/chain/sync')
def chain_syncing():
    valid = requests.get("{0}/chain/checkValidity".format(adresse_to_sync_with))
    if valid.status_code:
        response = requests.get("{0}/chain".format(adresse_to_sync_with))
        # we need to reconstruct the chain for now
        return "Chain synced [TODO : reconstruct the chain]", 200

    return "Cannot sync with an none valid chain", 400

@app.route('/nodes/sync')
def node_syncing():
    nodes = requests.get("{0}/nodes".format(adresse_to_sync_with))
    
    for val in nodes:
        blockchain.nodes.append(val)
    
    return "All nodes synced", 200

@app.route('/nodes')
def nodes():
    nodes = blockchain.nodes
    return jsonify(nodes)

@app.route('/compute/block/hash')
def computeExistingBlockHash():
    b = blockchain.chain[0]
    hash = blockchain.chain[0].computeHash(merkle=True)
    return jsonify(b.toJson(), hash)

@app.route('/test/insert/block')
def testInsertBlock():
    blockCreated = block.Block(len(blockchain.chain), "Isa", blockchain.chain[-1].hash, time.time())
    hash = blockchain.proofOfWork(blockCreated)
    blockCreated.hash = hash
    #blockchain.add_block(blockchain, hash)
    
    return jsonify(blockCreated.toJson(), hash)

if __name__ == "__main__":
    main()
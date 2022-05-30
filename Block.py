## import sha256 library, json, flask and time
from hashlib import sha256
from flask import Flask, request
import requests
import json
import time

## Create random strings to fill transactions
import random
import string

class Block:
    """
    Represents a single Block object
    """
    def __init__(self, index, transactions, timestamp, previous_hash, nonce = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
    
    def calculate_hash(self):
        """
        Return the hash of the block contents
        """
        block_data = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_data.encode()).hexdigest()


class Blockchain:
    """
    Represents a blockchain
    """
    # Difficulty of PoW (set to 5 for the best effect)
    difficulty = 5

    def __init__(self):
        """
        Build the Blockchain with an empty chain/list of unconfirmed transactions.
        Create the first block by calling create_genesis_block
        """
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generate the genesis block/first block of the blockchain
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, block):
        """
        Simulate the proof of work process by generating a hash that starts with the correct amount of 0's
        """
        block.nonce = 0
        calculated_hash = block.calculate_hash()
        
        while not calculated_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            calculated_hash = block.calculate_hash()
            print(calculated_hash)
        return calculated_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True
    
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.calculate_hash())
    
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)
    
    def mine(self):
        ## If there are no unconfirmed transactions, do nothing.
        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.last_block

        ## Create a new Block Object
        new_block = Block(index=last_block.index + 1, 
                            transactions=self.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=last_block.hash)
        
        ## Generate the PoW
        proof = self.proof_of_work(new_block)

        ## Add the new block (the proof is also checked here before the Block is added to the Blockchain)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index


"""
The below starts flask and enables you to start the blockchain and mine new blocks:
1. Start the .py file in command prompt "python Block.py".
2. Open a seperate cmd prompt window and run "curl http://127.0.0.1:5000/chain" to start a new Blockchain.
3. Then, run the command "curl http://127.0.0.1:5000/mine" to mine a new block.
"""

app = Flask(__name__)
blockchain = Blockchain()
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/mine', methods=['GET'])
def mine_a_block():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    blockchain.add_new_transaction(random_string)
    random_string = ''.join(random.choice(letters) for i in range(10))
    blockchain.add_new_transaction(random_string)
    random_string = ''.join(random.choice(letters) for i in range(10))
    blockchain.add_new_transaction(random_string)
    random_string = ''.join(random.choice(letters) for i in range(10))
    blockchain.add_new_transaction(random_string)
    random_string = ''.join(random.choice(letters) for i in range(10))
    blockchain.add_new_transaction(random_string)
    blockchain.mine()
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data[-1]})
    

app.run(debug=True, port=5000)
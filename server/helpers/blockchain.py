from web3 import Web3
from ethers import ethers
from typing import List
import json

class Blockchain(object):
    def __init__(self, private_key: str) -> None:
        with open("Profile.json", "r") as f:
            abi = json.load(f)
        
        self.address = ""
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/bf8cd18abd9e4daf8b0b552cdb8af09b"))
        self.contract = self.w3.eth.contract(address=abi["address"], abi=abi["abi"])

    def mint_nft(self, addresses: List[str], token_ids: List[int], roots: List[str]) -> str:
        transaction = self.contract.functions.mint(addresses, token_ids, roots).buildTransaction({
            "nonce": self.address,
            "gasPrice": ethers.utils.toWei("10", "gwei"),
            "gas": 1000000
        })
        return self.send_transaction(transaction=transaction)

    def update_nft_info(self, token_id: int, root: str, signature: str) -> str:
        transaction = self.contract.functions.updateMerkleRoot(token_id, root, signature).buildTransaction({
            "gasPrice": ethers.utils.toWei("10", "gwei"),
            "gas": 1000000
        })
        return self.send_transaction(transaction=transaction)


    def send_transaction(self, transaction) -> str:
        signed_transaction = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_transaction(signed_transaction)
        return str(tx_hash)
    
blockchain = Blockchain(private_key="")

from web3 import Web3
from ethers import ethers
from typing import List
import json

class Blockchain(object):
    def __init__(self, private_key: str) -> None:
        with open("Profile.json", "r") as f:
            abi = json.load(f)

        self.w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
        self.provider = ethers.providers.InfuraProvider(
            "INFURA_PROJECT_ID", "sepolia"
        )

        self.contract = Web3.eth.contract(contract_address=abi["address"], contract_abi=abi["api"], provider=self.provider)
        self.wallet = ethers.Account.from_key(private_key)

    def mint_nft(self, addresses: List[str], token_ids: List[int], merkle_roots: List[str]) -> str:
        transaction = self.contract.functions.mint(addresses, token_ids, merkle_roots).buildTransaction({
            "from": self.wallet.address,
            "gasPrice": ethers.utils.toWei("10", "gwei"),
            "gas": 1000000
        })
        return self.send_transaction(transaction=transaction)

    def update_nft_info(self, token_id: int, merkle_root: str) -> str:
        transaction = self.contract.functions.updateMerkleRoot(token_id, merkle_root).buildTransaction({
            "from": self.wallet.address,
            "gasPrice": ethers.utils.toWei("10", "gwei"),
            "gas": 1000000
        })
        return self.send_transaction(transaction=transaction)


    def send_transaction(self, transaction) -> str:
        signed_transaction = self.wallet.sign_transaction(transaction)
        tx_hash = self.provider.send_transaction(signed_transaction)
        return tx_hash
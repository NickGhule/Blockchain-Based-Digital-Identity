from web3 import Web3, HTTPProvider
import json


class BlockchainConnection:
    def __init__(self):
        # Connect to the blockchain
        host = '127.0.0.1'
        port = '8545'
        self.w3 = Web3(HTTPProvider('http://' + host + ':' + port))

        contractBuild = open("build/contracts/digitalID.json", "r").read()
        _abi = json.loads(contractBuild)['abi']

        # TODO: Change the address to the address of the contract
        # This address is the address of the contract which changes for every deployment
        _address = "0x68b6B273d4B7197ca4a1a192570CD7963771a558"

        self.contract = self.w3.eth.contract(address=_address, abi=_abi)

    def addDocument(self, _userName, _documentID,  _documentHash, _address=None):
        if _address == None:
            _address = self.w3.eth.accounts[0]
        tx_hash = self.contract.functions.addDocumentHash(
            _userName, _documentID, _documentHash).transact({'from': _address, 'gas': 1000000})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt

    def getDocumentHistory(self, _userName, _documentID):
        return self.contract.functions.getDocumentHashHistory(_userName, _documentID).call()


if __name__ == "__main__":
    bc = BlockchainConnection()
    # bc.addDocument("nickghule", "test", "test2")
    print(bc.getDocumentHistory("nickghule", "test"))

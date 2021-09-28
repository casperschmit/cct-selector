from web3 import Web3
import os

# TODO change contract addresses + private keys to the deployed contract

web3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/a15d9f6e6d4a468fa0ea89fb134d69f3"))

# the contract address and the ABI value set in the next cell need to be changed when
# the Solidity Code is changed and the conract is redeployed
contract_address = 'XYZ'
wallet_address = 'XYZ'  # actual address obfuscated
# the following data should not be made public under any circumstances when you working on the MainNET
# as this can be used to withdraw valuable Ethers from the wallet mentioned above
# here we make it public because the wallet is on a Test Chain (rinkbe) and the ether coins in the wallet have
# have no financial value
web3.eth.default_account = 'XYZ'

wallet_private_key = 'XYZ'  # actual private_key obfuscated

abi = None
with open(os.path.dirname(os.path.abspath(__file__)) + '/db_abi.txt', 'r') as f:
    abi = f.read()

db_contract = web3.eth.contract(address=contract_address, abi=abi)

with open(os.path.dirname(os.path.abspath(__file__)) + '/curator_abi.txt', 'r') as f:
    abi = f.read()

contract_address = 'XYZ'

curator_contract = web3.eth.contract(address=contract_address, abi=abi)

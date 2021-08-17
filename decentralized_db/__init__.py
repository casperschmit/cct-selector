import time
from web3 import Web3
import os

# web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/68ae8e6787934812814cffe521999999"))
web3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/a15d9f6e6d4a468fa0ea89fb134d69f3"))

# the contract address and the ABI value set in the next cell need to be changed when
# the Solidity Code is changed and the conract is redeployed
contract_address = '0xf6D77DED05d1F09e44cFB0cA71456C0Fe0b8A4b8'
wallet_address = '0x688fE02e313407F7fc1CF8A0a85113e129Eb10Af'  # actual address obfuscated

# the following data should not be made public under any circumstances when you working on the MainNET
# as this can be used to withdraw valuable Ethers from the wallet mentioned above
# here we make it public because the wallet is on a Test Chain (rinkbe) and the ether coins in the wallet have
# have no financial value

wallet_private_key = '3d524dd883f2b8d14c3aa157456cdecadacc506a17404aba31d4641483f651ba'  # actual private_key obfuscated

abi = None
with open(os.path.dirname(os.path.abspath(__file__)) + '/db_abi.txt', 'r') as f:
    abi = f.read()

db_contract = web3.eth.contract(address=contract_address, abi=abi)

with open(os.path.dirname(os.path.abspath(__file__)) + '/curator_abi.txt', 'r') as f:
    abi = f.read()

contract_address = '0xB45cC39ca3F4aC08A40b6e902AFf165BdaD366F3'

curator_contract = web3.eth.contract(address=contract_address, abi=abi)

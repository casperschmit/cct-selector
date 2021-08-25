from decentralized_db import db_contract, web3, curator_contract

if __name__ == '__main__':
    # print(db_contract.functions.getCCTName(22).call())
    # print(web3.isConnected())
    # print(web3.eth.blockNumber)
    # print(web3.eth.default_account)
    # print(curator_contract.functions.getProposedCCTs().call())
    # tx = curator_contract.functions.proposeCCT("newnewnew", 123445678).buildTransaction({
    #     'nonce': web3.eth.get_transaction_count(web3.eth.default_account)})
    # signed_tx = web3.eth.account.signTransaction(tx, private_key='3d524dd883f2b8d14c3aa157456cdecadacc506a17404aba31d4641483f651ba')
    # res = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    # receipt = web3.eth.waitForTransactionReceipt(signed_tx.hash)
    # print("Gas used:"+receipt.gasUsed)
    pass

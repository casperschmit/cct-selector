from decentralized_db import db_contract, web3, curator_contract

if __name__ == '__main__':
    # print(db_contract.functions.getCCTName(22).call())
    # print(curator_contract.functions.proposeCCT("newnew", 69))
    print(db_contract.functions.getAll().call())
    print(web3.isConnected())

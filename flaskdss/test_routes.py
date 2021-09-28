import random

from flask import render_template, request

from decentralized_db import curator_contract, web3
from flaskdss import application, db
from flaskdss.models import CCT

private_key = 'PLACEHOLDER'


@application.route('/centralized_write', methods=['GET', 'POST'])
def centralized_write():
    if request.method == 'POST':
        cct = CCT(
            name='test',
            whitepaper='test',
            docs='test',
            github='test',
            source_chain='test',
            source_permissions='test',
            target_chain='test',
            target_permissions='test',
            use_case='test',
            technical_scheme='test'
        )
        db.session.add(cct)
        db.session.commit()
    return render_template('home.html', title='test')


@application.route('/remove_tests', methods=['GET', 'POST'])
def remove_tests():
    if request.method == 'POST':
        ccts = CCT.query.filter_by(name='test').all()
        for cct in ccts:
            db.session.delete(cct)
    return render_template('home.html', title='test')


@application.route('/render_only', methods=['GET', 'POST'])
def render_only():
    return render_template('home.html', title='test')


@application.route('/centralized_read', methods=['GET', 'POST'])
def centralized_query():
    if request.method == 'POST':
        cct = CCT.query.filter_by(name='test').first()
    return render_template('home.html', title='test')


@application.route('/decentralized_read', methods=['GET', 'POST'])
def decentralized_read():
    if request.method == 'POST':
        curator_contract.functions.getProposedCCTs().call()
    return render_template('home.html', title='test')


@application.route('/decentralized_write', methods=['GET', 'POST'])
def decentralized_write():
    if request.method == 'POST':
        num = random.randint(1, 999999999999)
        print(num)
        try:
            tx = curator_contract.functions.proposeCCT("newnewnew", num).buildTransaction()
            signed_tx = web3.eth.account.signTransaction(tx,
                                                         private_key=private_key)
            res = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            receipt = web3.eth.waitForTransactionReceipt(signed_tx.hash)
            print("Gas used:" + str(receipt.gasUsed))
        except Exception as e:
            print(e)
            return render_template('home.html', title='test'), 403
    return render_template('home.html', title='test')

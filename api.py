from fastapi import FastAPI, Form
from uuid import uuid4
from models import create_session, Block, Transaction, User, Chain, asdict
from blockchain import hash, proof_of_work


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./blockchains.db'
db = SQLAlchemy(app)


@app.route('/mine', methods=['POST'])
def mine():
    values= request.get_json()
    sender = values['sender']
    with create_session(db.engine) as session:
        sender = User.get_by_id(session, 1)
        recipient = User.get_by_id(data['sender'])
        last_block = Chain.get_latest_block(session)
        last_proof = last_block.proof
        proof = proof_of_work(last_proof)
        Chain.new_transaction(sender=sender, recipient=recipient, amount=1.0)
        previous_hash = hash(asdict(last_block))
        block = Chain.new_block(session, proof, previous_hash)
        response = {
            'message': 'New Block Forged',
            'index': block.id,
            'transactions': block.transactions,
            'proof': block.proof,
            'previous_hash': block.previous_hash,
        }
    return jsonify(response), 200


@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    keys = {'sender', 'recipient', 'amount'}
    data = {u: v for u, v in values.items if u in keys}
    #Check that the required fields are in the POST'd data
    if len(data) < len(keys):
        return 'Missing Values', 400 

    with create_session(db.engine) as session:
        sender = User.get_by_id(session, data['sender'])
        recipient = User.get_by_id(data['recipient'])
        amount = data['amount']
        block_index = Chain.new_transaction(session, sender, recipient, amount)
    response = {'message': f'Transactions will be added to Block {block_index}'}
    return jsonify(response), 201


@app.route('/chain',  methods=['GET'])
def full_chain():
    with create_session(db.engine) as session:
        chain = [asdict(block) for block in Chain.get_all_blocks(session)]
        response = {
            'chain': chain,
            'length': len(chain)
        }
    return jsonify(response), 200


db.create_all()

with create_session(db.engine) as session:
    User.create_node_user(session)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
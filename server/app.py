# server/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)



@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Order messages by created_at in ascending order
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([message.serialize() for message in messages])

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.serialize()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def message_detail(id):
    message = Message.query.get_or_404(id)

    if request.method == 'PATCH':
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        return jsonify(message.serialize())

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)

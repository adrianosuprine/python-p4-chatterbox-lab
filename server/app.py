from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_serialized = [messages.to_dict() for messages in messages]
        response = jsonify(messages_serialized),200
        return response
    elif request.method == 'POST':
        body = request.json.get('body')
        username = request.json.get('username')
        
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()
        
        response = jsonify(new_message.to_dict()),201
        return response 
    
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error':'message not found'}), 404
    if 'body' in request.json:
        message.body = request.json['body']
    db.session.commit()
    return jsonify(message.to_dict())


@app.route('/messages/<int:id>', methods=['DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    db.session.delete(message)
    db.session.commit()
        
    return jsonify({'message': 'message delete successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555)

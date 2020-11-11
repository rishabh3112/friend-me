from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_cors import CORS
from joblib import load
import numpy as np

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = ['A', 'B', 'C']
users = {}
model = load('model.m')
features = ['age', 'movie', 'sports', 'travel']


def classify(user):
    X = []
    for feature in features:
      X.append(user[feature])
    X = np.array(X)
    X.reshape(1, -1)
    # return model.predict(X)[0]
    return 'A'


@app.route('/', methods=['POST'])
def home():
    user = {}
    data = request.json
    user['name'] = data['name']
    for feature in features:
        user[feature] = data[feature]
    user['room'] = classify(user)
    return jsonify(user)


@socketio.on('join')
def on_join(user):
    name = user['name']
    room = user['room']
    join_room(room)
    send(name + ' has entered the room.', room=room)


@socketio.on('leave')
def on_leave(user):
    name = user['name']
    room = user['room']
    leave_room(room)
    send(name + ' has left the room.', room=room)

@socketio.on('message')
def handle_message(data):
    send(data['message'], room=data['room'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

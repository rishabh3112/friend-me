from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_cors import CORS
from joblib import load
import numpy as np

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = ['A', 'B', 'C']
model = load('model.m')
features = ['age', 'movie', 'sports', 'travel']
cnt = 0

def classify(years,sprt,trvl,mov_num):
    arr = []
    if mov_num == 0:
        arr = [1,0,0,0]
    if mov_num == 1:
        arr = [0,1,0,0]
    if mov_num == 2:
        arr = [0,0,1,0]
    if mov_num == 3:
        arr = [0,0,0,1]
    
    inp = [years, sprt, trvl] + arr   
    ans = model.predict([inp])

    if ans == 0:
        ans = 'A'
    elif ans == 1:
        ans = 'B'
    elif ans == 2:
        ans = 'C'        

    print(ans)
    return(ans)


@app.route('/', methods=['POST'])
def home():
    global cnt
    user = {}
    data = request.json
    user['name'] = data['name']
    for feature in features:
        user[feature] = data[feature]
    user['room'] = classify(user['age'], user['sports'], user['travel'], user['movie'])
    user['id'] = cnt
    cnt = cnt + 1
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

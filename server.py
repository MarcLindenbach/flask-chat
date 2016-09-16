from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import uuid


app = Flask(__name__)
app.secret_key = 'K33p-1t-S3cr3t-k33p-1t-s4f3'
socketio = SocketIO(app)

def emit_user_list():
    emit('users_updated', users, broadcast=True)

@app.route('/')
def index():
    if 'uid' not in session:
        session['uid'] = str(uuid.uuid4())
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    pass

@socketio.on('disconnect')
def on_disconnect():
    pass

@socketio.on('message')
def on_message(event_name, user_name):
    pass

if __name__ == '__main__':
    socketio.run(app, debug=True)

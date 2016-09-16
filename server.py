from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
from werkzeug.contrib.cache import SimpleCache
import uuid


app = Flask(__name__)
app.secret_key = 'K33p-1t-S3cr3t-k33p-1t-s4f3'
socketio = SocketIO(app)
cache = SimpleCache()


def emit_user_list():
    emit('user_list', cache.get('user_list'), broadcast=True)

def emit_chat_message(user_name, chat_message):
    emit('chat_message', {'chat_message': chat_message, 'user_name': user_name}, broadcast=True)

@app.route('/')
def index():
    if 'uid' not in session:
        session['uid'] = str(uuid.uuid4())

    user_list = cache.get('user_list')
    if user_list is None or not session['uid'] in user_list:
        user_name = ''
    else:
        user_name = user_list[session['uid']]['name']

    return render_template('index.html', user_name=user_name)

@socketio.on('connect')
def on_connect():
    user_list = cache.get('user_list')

    if user_list is None:
        user_list = {}

    if not session['uid'] in user_list:
        user_list[session['uid']] = {
            'name': 'Anonymous',
            'connections': 1
        }
    else:
        user_list[session['uid']]['connections'] += 1

    cache.set('user_list', user_list)
    emit_user_list()

@socketio.on('disconnect')
def on_disconnect():
    user_list = cache.get('user_list')

    if user_list is None:
        return

    if not session['uid'] in user_list:
        return

    user_list[session['uid']]['connections'] -= 1
    if user_list[session['uid']]['connections'] == 0:
        del user_list[session['uid']]
    cache.set('user_list', user_list)
    emit_user_list()

@socketio.on('message')
def on_message(event_name, message_text):
    user_list = cache.get('user_list')

    if not session['uid'] in user_list:
        user_name = ''
    else:
        user_name = user_list[session['uid']]['name']

    if event_name == 'send_chat_message':
        emit_chat_message(user_name, message_text)
        return

    if event_name == 'change_user_name':
        user_list[session['uid']]['name'] = message_text
        cache.set('user_list', user_list)
        emit_user_list()


if __name__ == '__main__':
    socketio.run(app, debug=True)

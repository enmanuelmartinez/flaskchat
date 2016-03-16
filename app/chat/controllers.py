from flask import Blueprint, render_template
from app import socketio, app


mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

# SocketIO

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('join')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('leave')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('close room')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])

@socketio.on('connect')
def test_connect():
    emit('message', {'data': 888888})
    emit('klk', {'data': 42})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    pass
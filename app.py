# -*- coding: UTF-8 -*-
from flask import Flask, render_template, session, redirect, url_for, escape, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

from forms import LoginForm

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'

async_mode = None
'''if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)'''

socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method is 'POST':
        return 'login POST'
    elif request.method is 'GET':
	return 'login GET'
    
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# SocketIO

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


if __name__ == "__main__":
    socketio.run(app, debug=True)

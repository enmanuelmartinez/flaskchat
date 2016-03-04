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

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    pass


if __name__ == "__main__":
    socketio.run(app, debug=True)

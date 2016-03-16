# -*- coding: UTF-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO

# Define the WSGI application object
app = Flask(__name__, static_url_path='/static')

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


async_mode = None
if async_mode is None:
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

    print('async_mode is ' + async_mode)


socketio = SocketIO(app, async_mode=async_mode)

# Import a module / component using its blueprint handler variable (mod_auth)
from app.auth.controllers import mod_auth as auth_module
from app.chat.controllers import mod_chat as chat_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(chat_module)


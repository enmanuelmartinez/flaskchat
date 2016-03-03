# -*- coding: UTF-8 -*-

from flask import Flask, render_template, session, redirect, url_for, escape, request
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


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


if __name__ == "__main__":
    app.run(debug=True)

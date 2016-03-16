# -*- coding: UTF-8 -*-

from app import app, socketio
    
socketio.run(app, host='127.0.0.1', port=5000, debug=True)
#app.run()
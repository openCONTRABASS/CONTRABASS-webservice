"""
    This file is part of CONTRABASS-webservice project.
    Copyright (C) 2020-2021  Alex Oarga  <718123 at unizar dot es> (University of Zaragoza)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import eventlet
eventlet.monkey_patch()

import os
import logging
import logging.config

from flask import Flask, jsonify, session, request
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from flask_socketio import join_room

from dotenv import load_dotenv
from celery.result import AsyncResult

from flasgger import Swagger

from .constants import SESSION_ROOM_ID_KEY
from .database import db

from .celery_app import celery_app

from .blueprints.submit.submit_bp import submit_bp
from .blueprints.models.models_bp import models_bp
from .blueprints.results.results_bp import results_bp
from .blueprints.websockets.websockets_bp import websockets_bp

from .exception_handler import init_exception_handler

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../../.env'))


LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# Logger config
logging.config.dictConfig(app.config["DICT_LOGGER"])

# Database config

# MONGODB
'''
from .database import db

app.config['MONGODB_SETTINGS'] = {
    'db': '',
    'host': '',
    'port': ,
    'alias': ''
}
db.init_app(app)
'''
# MYSQL
db.init_app(app)

LOGGER.info("Successfully init db connection")

# Swagger config
app.config['SWAGGER'] = {
    'title': 'CONTRABASS API',
    'uiversion': 3
}
Swagger(app, template_file='swagger.yml')
LOGGER.info("Successfully init Swagger")

# Register blueprints
app.register_blueprint(submit_bp, url_prefix='/')
app.register_blueprint(models_bp, url_prefix='/')
app.register_blueprint(results_bp, url_prefix='/')
app.register_blueprint(websockets_bp, url_prefix='/')
LOGGER.info("Successfully init blueprints")

# Register exception handlers
init_exception_handler(app)
LOGGER.info("Successfully init exception handlers")

# Add CORS
CORS(app)

# Init websockets
socketio = SocketIO(app, \
                    cors_allowed_origins='*', \
                    logger=True, \
                    engineio_logger=True, \
                    message_queue=app.config['REDIS_BROKER_URL'])


@app.errorhandler(404)
def page_not_found(e):
    #return render_template('404.html'), 404
    response = jsonify({'message': "Not found"})
    response.status_code = 404
    return response

@app.route('/hola/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@socketio.on('connect')
def test_connect():
    LOGGER.info("Client connected via websocket")

@socketio.on('join')
def on_join(room_name):
    LOGGER.info(f"socket.io/join {room_name}")
    join_room(room_name)

if __name__ == '__main__':
    socketio.run(app)

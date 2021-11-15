from flask_socketio import SocketIO, send, emit
from celery.utils.log import get_task_logger

LOGGER = get_task_logger(__name__)

socketio = SocketIO(message_queue='redis://')


def send_message_client(room_name, message):
    socketio.emit(room_name, {'data': message}, to=room_name, room=room_name)

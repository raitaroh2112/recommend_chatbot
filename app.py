from flask import Flask, render_template
from flask_socketio import SocketIO
from chat import generate_response

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    response_data = generate_response(user_message)

    socketio.emit('bot_response', response_data)


if __name__ == '__main__':
    socketio.run(app, port=3000)

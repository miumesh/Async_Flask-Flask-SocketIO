from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True

socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()

def barcodegenerator():
    print("Making random numbers")
    while not thread_stop_event.is_set():
        number = round(random()*10, 3)
        print(number)
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')
    if not thread.is_alive():
        print("Starting Thread")
        thread = Thread(target = barcodegenerator)
        thread.start()

if __name__ == '__main__':
    socketio.run(app)

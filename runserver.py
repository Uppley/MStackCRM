import os
from os import path
from celery import Celery
from angular_flask import app
from flask_socketio import send, emit, SocketIO
import atexit


import sys
import zmq
from multiprocessing import Process
import multiprocessing as mp
import time

socketio = SocketIO(app)


def img_worker():
    # Lurk activate and lurk through video through here
    context = zmq.Context()

    ventilator_send = context.socket(zmq.PUSH)
    ventilator_send.bind("tcp://127.0.0.1:5557")
    # Activate the while true functionality
    while True:
        rd_int = random.randint(1,1000)
        if(rd_int < 50):
            ventilator_send.send("MESSAGE {}".format(rd_int))
            time.sleep(1)

def img_puller():
    context = zmq.Context()
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:5557")
    count = 0
    while True:
        message = work_receiver.recv()
        if(message is not None):
            print message
        count += 1


def main():
    mp.Process(target=img_worker, args=()).start()
    mp.Process(target=img_puller, args=()).start()


extra_dirs = ['angular_flask/static', ]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)


def removeProcesses():
    while True:
        time.sleep(1)
        if not mp.join():
            break


def runserver():
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port,
                 extra_files=extra_files, debug=True)
    # app.run(host='0.0.0.0', port=port, extra_files=extra_files, debug=True)

if __name__ == '__main__':
    atexit.register(removeProcesses)
    main()
    runserver()

import sys
import zmq
from  multiprocessing import Process
import time

def worker():
    # Lurk through video through here
    context = zmq.Context()
    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect("tcp://127.0.0.1:5557")

    for task_nbr in range(10000000):
        message = work_receiver.recv()

    sys.exit(1)

def main():
    Process(target=worker, args=()).start()
    context = zmq.Context()
    ventilator_send = context.socket(zmq.PUSH)
    ventilator_send.bind("tcp://127.0.0.1:5557")
    for num in range(10000000):
        ventilator_send.send("MESSAGE")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    msg_per_sec = 10000000 / duration

    print "Duration: %s" % duration
    print "Messages Per Second: %s" % msg_per_sec

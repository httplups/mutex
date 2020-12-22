#!/usr/bin/env python3

import socket
import urllib.request
import json
import sys
import signal
from contextlib import contextmanager
import time

global end_time
end_time = False

@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    print('End of time')

    global end_time
    end_time = True

    raise TimeoutError

def local_time(counter):
    return ' (LAMPORT_TIME={})'.format(counter)

def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1

def event(counter):
    counter += 1
    print('Something happened here... at {}'.format(local_time(counter)))
    return counter

def connect(counter, sock, HOST, PORT):
    s.connect((HOST, PORT))
    counter += 1
    print('Connection Request at {}'.format(local_time(counter)))
    return counter

def send_message(server_ip, counter, sock):
    counter += 1
    message = 'Hello'
    data = json.dumps({"message":message, "timestamp":counter})
    s.send(data.encode())
    print('Message sent to {} at {}'.format(server_ip, local_time(counter)))
    return counter

def recv_message(server_ip, counter, sock):
    data = sock.recv(1024)
    data = json.loads(data.decode())
    # message = data.get("message")
    timestamp = data.get("timestamp")
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received from {} at {}'.format(server_ip,local_time(counter)))
    return counter

def get_permission(server_ip, sock):
    file = 'bd.txt'
    data = json.dumps({"GET":file})

    
    s.send(data.encode())
    print('Trying to get permission...')

    # Add a timeout block.
    with timeout(5):
        resp = s.recv(1024)
        print(resp)
        if (resp == "Denied"):
            print('Denied')
        if (resp == "OK"):
            print('I am writing on the file...')



def my_func():
    # Add a timeout block.
    with timeout(5):
        print('entering block')
        time.sleep(10)
        print('This should never get printed because the line before timed out')

if __name__ == '__main__': 
    HOST = sys.argv[1]
    PORT = 8888        # The port used by the server
    counter = 0
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print('This IP address is: ', external_ip)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        get_permission(HOST, s)
        
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)

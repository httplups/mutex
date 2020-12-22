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

def get_permission(server_ip, sock):
    data = json.dumps({"type":"GET"})

    
    s.send(data.encode())
    print('Trying to get permission...')

    # Add a timeout block.
    with timeout(5):
        resp = s.recv(1024)
        print(resp)
        if (resp == "Denied"):
            print('Denied')
        if (resp == "Allowed"):
            print('I am writing on the file...')


if __name__ == '__main__': 
    HOST = sys.argv[1]
    PORT = 8888        # The port used by the server
    
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print('This IP address is: ', external_ip)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        get_permission(HOST, s)
        
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)

#!/usr/bin/env python3

import socket
import urllib.request
import json
import sys
import signal
from contextlib import contextmanager
import time
import _thread as thread
from threading import Thread

global end_time
end_time = False

@contextmanager
def timeout(time, server_ip, sock):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        get_permission(server_ip, sock)
    # finally:
    #     # Unregister the signal so it won't be triggered
    #     # if the timeout is not reached.
    #     signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    global end_time
    end_time = True

    raise TimeoutError

def mytimeout(server_ip, sock):
    time.sleep(5)
    print('irei chamar funcao dnv')
    return True

def get_permission(server_ip, sock):

    timeout = True

    data = json.dumps({"type":"GET"})

    
    s.send(data.encode())
    print('Trying to get permission...')

    
    print('sera q printa')
    # Add a timeout block.
    # with timeout(1, server_ip, sock):
    while (timeout):
        resp = (s.recv(1024)).decode()
        print(resp)
        if (resp == "Denied"):
            print('Denied')
            break
        if (resp == "Allowed"):
            print('I am writing on the file...')
            time.sleep(5)
            s.send("FREE".encode())
            break


if __name__ == '__main__': 
    HOST = sys.argv[1]
    PORT = 8888        # The port used by the server
    
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print('This IP address is: ', external_ip)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        


        import multiprocessing 
        p1 = multiprocessing.Process(target=mytimeout, args=(HOST, s)) 
        p1.start() 
        p2 = multiprocessing.Process(target=get_permission, args=(HOST, s)) 
        p2.start() 
        
        # t1 = Thread(target=mytimeout, args=(HOST, s))
        # t1.start()
        # t2 = Thread(target=get_permission, args=(HOST, s))
        # t2.start()
        
        p1.join()
        p2.terminate()
        p2.kill()
        print('p1 finishes')
        print(p2.is_alive())
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)

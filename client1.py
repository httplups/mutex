#!/usr/bin/env python3

import socket
import urllib.request
import json
import sys

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

if __name__ == '__main__': 
    HOST = sys.argv[1]
    PORT = 8888        # The port used by the server
    counter = 0
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print('This IP address is: ', external_ip)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        counter = connect(counter, s, HOST, PORT)
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)

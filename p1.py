#!/usr/bin/env python3

import socket
import urllib.request
import json
import sys
import time

def get_permission(server_ip, sock):

    data = json.dumps({"type":"GET"})
    s.send(data.encode())
    print('Trying to get permission...')

    while (True):
        resp = (s.recv(1024)).decode()
        print(resp)
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
        get_permission(HOST, s)
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)

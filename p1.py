#!/usr/bin/env python3

import socket
import urllib.request
import json
import sys
import time

def get_permission(server_ip, sock, sec):

    sock.send("GET".encode())
    print('Trying to get permission...')

    while (True):
        resp = (sock.recv(1024)).decode()
        print(resp)
        if (resp == "Allowed"):
            print('I am doing something with the file...')
            time.sleep(sec)
            sock.send("FREE".encode('utf-8'))
            sock.close()
            break


if __name__ == '__main__': 
    HOST = sys.argv[1]
    PORT = 8888        # The port used by the server
    second_with_file = int(sys.argv[2])

    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print('This IP address is: ', external_ip)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        get_permission(HOST, s, second_with_file)
        print('Terminou')
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)
        # counter = send_message(HOST, counter, s)
        # counter = recv_message(HOST, counter, s)

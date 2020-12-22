import socket
import os
import _thread as thread
import time
import json
import sys
global queue_file
queue_file = list()

def insert_element(peer):
    print('Inserted', peer)
    global queue_file
    queue_file.append(peer)

def remove_element(peer):
    print('Removed', peer)
    global queue_file
    queue_file.remove(peer)

def check_queue(peer):
    if ((not queue_file) or (queue_file.index(peer) == 0)):
        # if list is empty or the peer is on top of the list 
        return 1
    else:
        return 0

# response - 1 -> allowed 
# response - 0 -> waiting for CS
# response - 2 -> already used / free
def recv_request(peer, sock, stop_loop):
    response = 0
    try:
        data = sock.recv(1024)
        option = (data.decode())
        print(option)

        if (option == "GET"):

            insert_element(peer)

            response = check_queue(peer)
            # else:
            #     return "Denied"

        elif (option == "FREE"):
            print('liberando da fila')
            remove_element(peer)
            response = 2

    except ValueError:
        # acabou os bytes
        stop_loop = True
    return [stop_loop, response]

def send_message(sock):
    sock.send("Allowed".encode())

def handle_client(sock, peer):
    stop_loop = False
    with sock:
        while not stop_loop:
            stop_loop, response = recv_request(peer, sock, stop_loop)

            if stop_loop:
                break
        
            if (response == 1):
                # if allowed, send response
                send_message(sock)
            elif (response == 0):
                # it's not available
                while True:
                    if(check_queue(peer)):
                        break
                # now its available, then send response
                send_message(sock)
            else:
                # now its free for others to use
                continue
        sock.close()
    
def main():
    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
    PORT = 8888        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Coordinator started!')
        print('Waiting for requests...')
        while True:
            conn, addr = s.accept()
            # host, port = s.getpeername()
            print(addr)
            thread.start_new_thread(handle_client,(conn,addr))
        s.close()

if __name__ == '__main__': 

    try:
        main()
    except KeyboardInterrupt:
        print('Bye bye...')
        sys.exit(0)
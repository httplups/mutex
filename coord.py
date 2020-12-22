import socket
import os
import _thread as thread
import time
import json
import sys
global queue_file
queue_file = list()

def insert_element(peer):
    global queue_file
    queue_file.append(peer)

def remove_element(peer):
    global queue_file
    queue_file.remove(peer)

def recv_request(peer, sock, stop_loop):

    try:
        data = sock.recv(1024)
        data = json.loads(data.decode())
        option = data.get("type")

        if (option == "GET"):

            insert_element(peer)

            if ((not queue_file) or (queue_file.index(peer) == 0)):
                # if list is empty or the peer is on top of the list 
                response = "Allowed"
            # else:
            #     return "Denied"

        elif (option == "FREE"):
            print('liberando da fila')
            remove_element(peer)
            response = ""

    except ValueError:
        # acabou os bytes
        stop_loop = True
        response = ""
    return [stop_loop, response]

def handle_client(sock, peer):
    stop_loop = False
    with sock:
        while not stop_loop:
            stop_loop, response = recv_request(peer, sock, stop_loop)

            if stop_loop:
                break
            
            time.sleep(5)
            sock.send(response.encode())
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
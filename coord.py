import socket
import os
import _thread as thread
import time
import json
import sys
global queue_file
queue_file = list()

def show_queue():
    print(queue_file)

def insert_element(peer):
    print('Inserted', peer)
    global queue_file
    queue_file.append(peer)
    show_queue()

def remove_element(peer):
    print('Removed', peer)
    global queue_file
    queue_file.remove(peer)
    show_queue()

def check_queue(peer):
    if ((not queue_file) or (queue_file.index(peer) == 0)):
        # if list is empty or the peer is on top of the list 
        return 1
    else:
        return 0   
                
def send_message(sock):
    sock.send("Allowed".encode('utf-8'))

def handle_client(sock, peer):
    with sock:
        while True:
            # read request
            data = sock.recv(1024)
            if not data:
                break
       
            option = (data.decode())

            if (option == "GET"):
                # its available
                insert_element(peer)
                if(check_queue(peer)):
                    send_message(sock)
                else:
                    # it's not available
                    while True:
                        print('checando sempre')
                        if(check_queue(peer)):
                            # now its available, then send 'allowed'
                            send_message(sock)
                            break

            elif (option == "FREE"):
                remove_element(peer)
            
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
            thread.start_new_thread(handle_client,(conn,addr))
        s.close()

if __name__ == '__main__': 

    try:
        main()
    except KeyboardInterrupt:
        print('Bye bye...')
        sys.exit(0)
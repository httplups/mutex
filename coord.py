import socket
import os
import _thread as thread
import time
import json
import sys

def recv_message(client_ip, sock, stop_loop):
    try:
        data = sock.recv(1024)
        data = json.loads(data.decode())
        # message = data.get("message")
        timestamp = data.get("timestamp")
    except ValueError:
        # acabou os bytes
        stop_loop = True
    return stop_loop

# usa counter como uma variavel global
def handle_client(conn, peer_ip):
    stop_loop = False
    with conn:
        # while not stop_loop:
        #     stop_loop = recv_message(client_ip, conn, stop_loop)
        #     if stop_loop:
        #         break
        #     send_message(client_ip, conn)
        conn.close()
    
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
            host, port = s.getpeername()
            print(addr, host, port)
            thread.start_new_thread(handle_client,(conn,addr))
        s.close()

if __name__ == '__main__': 

    try:
        main()
    except KeyboardInterrupt:
        print('Bye bye...')
        sys.exit(0)
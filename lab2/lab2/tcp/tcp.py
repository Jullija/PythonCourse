#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1970        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept() #nasłuchuje połączenia
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            # data = str(data,'utf-8')
            if data=='q':
                break
            print(data)
            # conn.sendall(data)

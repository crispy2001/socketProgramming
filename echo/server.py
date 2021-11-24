#!/usr/bin/python3
import socket
import _thread
from threading import *

HOST = 'localhost'
PORT = 8081

# create socket ans assigned socket.AF_INET(TCP) as the protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsocketopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)

print("server start at: " + HOST + ":" + str(PORT))
print("wair for connection...")


def clientThread(conn):
	while True:
		input_data = conn.recv(1024)
		if len(input_data) == 0:	# if connection closed
			conn.close()
			print("client closed connection.")
			break
		print("recv: " + input_data.decode())

		output_data = "echo " + input_data.decode()
		conn.send(output_data.encode())

while True:
	conn, addr = s.accept()
	print("connected by " + str(addr))

	_thread.start_new_thread(clientThread, (conn, ))
s.close()

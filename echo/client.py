#!/usr/bin/python3
import socket

HOST = 'localhost'
PORT = 8081

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
	output_data = input("please input message: ")
	print("send: " + output_data)
	s.send(output_data.encode())

	input_data = s.recv(1024)
	if len(input_data) == 0:
		s.close()
		print("server closed connection")
		break
	print("recv: " + input_data.decode())




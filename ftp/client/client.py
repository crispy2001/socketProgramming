#!/usr/bin/python3
import socket, os
import hashlib

client = socket.socket()
client.connect(('localhost',9999))

def download(cmd):
	client.send(cmd.encode()) #傳送命令，形式 get filename
	server_response = client.recv(1024) #接收檔案大小資訊
	print("servr response:",server_response)
	client.send(b"ready to recv file") #傳送確認資訊。
	file_total_size = int(server_response.decode()) #將檔案大小int化。
	received_size = 0 #初始化接收資料大小，為0
	filename = cmd.split()[1] #獲取檔名
	f = open(filename + ".new","wb") #以二進位制形式寫入
	m = hashlib.md5() #為md5準備

	while received_size != file_total_size:
	#'''下面的if判斷是用來完整接收檔案，從而避免粘包。'''
		if file_total_size - received_size > 1024: # 要收不止一次 24 
			size = 1024 
		else: # 最後一次了，剩多少收多少 
			size = file_total_size - received_size 
			print("last receive:",size) 
		data = client.recv(size) #data只需要是一小個記憶體，大小為1k就好 
		received_size += len(data) 
		m.update(data) #不斷更新md5 
		f.write(data) #不斷寫入 
		print(file_total_size, received_size) 

	new_file_md5 = m.hexdigest() #獲取十六進位制的md5 
	print("file recv done",received_size,file_total_size) 
	f.close()
	server_file_md5 = client.recv(1024) #接收md5值 
	print("server file md5:",server_file_md5) 
	print("client file md5:",new_file_md5) 

while True:
	cmd = input(">> :").strip() #形式 get filename
	if len(cmd) == 0: 
		client.close()
		print("client closed connection")
		break
	if cmd.startswith("get"):
		download(cmd)

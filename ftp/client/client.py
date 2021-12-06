#!/usr/bin/python3
import socket, os
import hashlib

client = socket.socket()
client.connect(('localhost',9992))

def download(filename):					# 從遠端下載檔案
	server_response = client.recv(1024) # 接收檔案大小資訊
	client.send(b"ready to recv file") # 傳送確認資訊
	file_total_size = int(server_response.decode()) # 檔案大小int化
	received_size = 0 # 初始化接收資料大小，為0
	f = open(filename + ".download", "wb") # 以二進位制形式寫入
	m = hashlib.md5() # 為md5準備，來確保我下載和遠端的檔事是不是真的是一樣的，沒有在唬你

	while received_size != file_total_size:
		if file_total_size - received_size > 1024: # 檔案太大，要收不止一次 1024
			size = 1024 
		else: # 最後一次了，剩多少收多少 
			size = file_total_size - received_size 
			# print("last receive:",size) 
		data = client.recv(size) # data只需要是一小個記憶體，大小為1k就好 
		received_size += len(data) 
		m.update(data) # 不斷更新md5 
		f.write(data) # 不斷寫入 
		#print(file_total_size, received_size) 

	new_file_md5 = m.hexdigest() # 獲取十六進位制的md5 
	print("download complete") 
	f.close()
	server_file_md5 = client.recv(1024) # 接收md5值 
	print("server file md5:",server_file_md5.decode()) 	# 證明我的兩邊的檔案是一樣的
	print("client file md5:",new_file_md5) 

def upload(filename):
	if os.path.isfile(filename):  # 判斷是否該檔名為檔案
		f = open(filename,"rb")
		m = hashlib.md5() # 為md5準備
		file_size = os.stat(filename).st_size # 利用os.stat獲取檔案的大小
		client.send( str(file_size).encode() ) # send file size
		client.recv(1024) # 等待確認，同時可以防止粘包。
		for line in f: # 一行一行傳送資料，同時更新md5
			m.update(line)  # 不斷更新md5
			client.send(line) # 不斷送資料。
		# print("file md5: ",m.hexdigest()) # 十六進位制的md5
		f.close()
		client.send(m.hexdigest().encode()) # send md5
		print("upload complete")
	else:
		print("no such a file")
def clientCMD(c):
	os.system(c)

def serverCMD():
	cmd = client.recv(1024).decode()
	print(cmd)

while True:
	data = input("input command: ")		
	cmd = data.split()
	if len(data) == 0: 
		client.close()
		print("client closed connection")
		break
	
	if cmd[0] == "DOWNLOAD":
		client.send(data.encode()) 
		download(cmd[1])
	elif cmd[0] == "UPLOAD":
		client.send(data.encode()) 
		upload(cmd[1])
	elif cmd[0] == "CLIENT":
		c = data[7:]
		clientCMD(c)
	elif cmd[0] == "SERVER":
		c = data[7:]
		client.send(c.encode()) 
		serverCMD()
	else:
		print("invalid input")
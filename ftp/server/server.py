#!/usr/bin/python3
import hashlib
import socket, os, time, _thread, subprocess
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost',9992))
server.listen(10)

def download(conn, filename):
	print(filename)
	if os.path.isfile(filename):  # 判斷是否該檔名為檔案
		f = open(filename ,"rb")
		m = hashlib.md5() # 為md5準備
		file_size = os.stat(filename).st_size # 利用os.stat獲取檔案的大小
		conn.send( str(file_size).encode() ) # send file size
		conn.recv(1024) 
		for line in f: # 一行一行傳送資料，同時更新md5
			m.update(line)  # 不斷更新md5
			conn.send(line) # 不斷送資料。
		print("file md5",m.hexdigest()) # 十六進位制的md5
		f.close()
		conn.send(m.hexdigest().encode()) # send md5
		print("send done")
	else:
		print("no such a file")

def upload(conn, filename):
	server_response = conn.recv(1024) # 接收檔案大小資訊
	conn.send(b"ready to recv file") # 傳送確認資訊
	file_total_size = int(server_response.decode()) #檔案大小
	received_size = 0 # 初始化接收資料大小，為0
	f = open(filename + ".upload","wb") # 以二進位制形式寫入
	m = hashlib.md5() # 為md5準備

	while received_size != file_total_size:
		if file_total_size - received_size > 1024:
			size = 1024 
		else: # 最後一次了，剩多少收多少 
			size = file_total_size - received_size 
			print("last receive:",size) 
		data = conn.recv(size) 
		received_size += len(data) 
		m.update(data) # 不斷更新md5 
		f.write(data) # 不斷寫入 

	new_file_md5 = m.hexdigest() # 獲取十六進位制的md5 
	print("file recv done") 
	f.close()
	server_file_md5 = conn.recv(1024) # 接收md5值 

def shCMD(cmd):
	output = subprocess.getoutput(cmd.decode())
	print(output)
	if output == '':
		print("output = none")
		conn.send(" ".encode())
	else:
		conn.send(output.encode())
	print("syscall complete")


def clientThread(conn):
	while True:
		print("wait for new command...")
		data = conn.recv(1024)
		if not data:
			print("client closed")
			break
		cmd = data.decode().split()
		if cmd[0] == "DOWNLOAD":
			download(conn, cmd[1])
		elif cmd[0] == "UPLOAD":
			upload(conn, cmd[1])
		else:
			shCMD(data)
		
while True:
	conn, addr = server.accept()
	print("connected by " + str(addr))
	_thread.start_new_thread(clientThread, (conn, ))
server.close()

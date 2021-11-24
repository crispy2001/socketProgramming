import hashlib
import socket,os,time
server = socket.socket()
server.bind(('localhost',9999))
server.listen()
while True:
	print("I am waiting for connection.")
	conn,addr = server.accept()
	print("new conn:",addr)
	while True:
		print("等待新指令")
		data = conn.recv(1024)
		if not data:
			print("客戶端已斷開")
			break
		cmd,filename = data.decode().split()
		print(filename)
		if os.path.isfile(filename):  #判斷是否該檔名為檔案
			f = open(filename,"rb")
			m = hashlib.md5() #為md5準備
			file_size = os.stat(filename).st_size #利用os.stat獲取檔案的大小
			conn.send( str(file_size).encode() ) #send file size
			conn.recv(1024) #等待確認，同時可以防止粘包。
			for line in f: #一行一行傳送資料，同時更新md5
				m.update(line)  #不斷更新md5
				conn.send(line) #不斷髮送資料。
			print("file md5",m.hexdigest()) #十六進位制的md5
			f.close()
			conn.send(m.hexdigest().encode()) #send md5
		print("send done")
server.close()

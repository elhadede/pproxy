import socket,threading,re,ssl,sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((str(sys.argv[1]),int(sys.argv[2])))
sock.listen(5)
def recvall(sock):
    BUFF_SIZE = 4096
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data
def syncer(s1,s2):
	while True:
		old = recvall(s2)
		print(old)
		s1.sendall(old)
def servant(c):
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	full = recvall(c)
	try:
		string = str(full.decode())
		print(string)
	except Exception:
		print("NO DECODE")
	if string.startswith("GET"):
		who = re.search(r'Host: (.*?)\r\n',string).group(1)
		print(":"+who+":")
		s.connect((who,80))
		s.sendall(full)
		final = recvall(s)
		print(final)
		c.sendall(final)
	elif string.startswith("CONNECT"):
		who = re.search(r'Host: (.*?)\r\n',string).group(1).split(":")[0]
		print(":"+who+":")
		s.connect((who,443))
		c.sendall(b'HTTP/1.1 200 Connection established\r\n\r\n')
		threading.Thread(target=syncer,args=[c,s]).start()
		threading.Thread(target=syncer,args=[s,c]).start()
		while True:
			pass

while True:
	i,ip = sock.accept()
	threading.Thread(target=servant,args=[i]).start()

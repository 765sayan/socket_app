import socket
import threading

threads = []

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
Address = (SERVER, PORT)
Disconnect_msg = 'DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(Address)

def handle_client(conn, addr):
	print(f'New connetion {addr} connected')
	#print(conn.getpeername())
	connected = True
	# for i in range(len(threads)):
	# 	connection = threads[i]
	# 	ad = connection.getpeername()
	# 	print(ad[1])
	while connected:
		msg_length = conn.recv(64).decode('UTF-8') #The first message is telling us the length of the message
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode('UTF-8')
			index = 0
			if msg == Disconnect_msg:
				connected = False
			print(addr[0])
			print(f'{addr} {msg}')
			conn.send('message recieved'.encode('UTF-8'))
			if str(msg) == 'chat':
				msg_length = conn.recv(64).decode('UTF-8')
				if msg_length:
					msg_length = int(msg_length)
					msg = conn.recv(msg_length).decode('UTF-8')
					port = int(msg)
					add = (SERVER, port)
					conn.send('Chat '.encode('UTF-8'))
					for i in range(len(threads)):
						connection = threads[i]
						ad = connection.getpeername()
						if ad[1] == port:
							index = i
					loopstate = True
					while loopstate == True:
						msg_length = conn.recv(64).decode('UTF-8')
						if msg_length:
							msg_length = int(msg_length)
							msg = conn.recv(msg_length).decode('UTF-8')
							if msg == 'cancel':
								loopstate = False
							print(threads[index])
							print(msg)
							# server.sendto(msg.encode('UTF-8'), add)
							msg = msg.encode('UTF-8')
							message_length = len(msg)
							leng = str(message_length).encode('UTF-8')
							leng = leng + b' '*(64-len(leng))
							threads[index].send(leng)
							threads[index].send(msg)


	threads.remove(conn)
	conn.close()

def start():
	server.listen()
	print(f'server is listening on {SERVER}')
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr)) #The Thread target is the name of the function and args are the arguments that is passed in the function
		thread.start()
		threads.append(conn)
		print(f'Active connectios - {threading.active_count() - 1}') #We are checking the amount of clients connected and subtracting the thread on which the server is running

print('Server is starting')
start()		
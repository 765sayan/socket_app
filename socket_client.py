import socket

PORT = 5000
Disconnect_msg = 'DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())

Address = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(Address)





def send(msg):
	
	message = msg.encode('UTF-8')
	msg_length = len(message)
	send_length = str(msg_length).encode('UTF-8')
	send_length = send_length + b' ' *(64 - len(send_length)) 
	client.send(send_length)
	client.send(message)
	# print(client.recv(2048).decode('UTF-8'))






work = input('Send press 1 and recieve press 0 - ')
if work == '1':
	loopState = True
	while loopState:


		msg = input('send message: ')
		if msg == 'DISCONNECT':
			loopState = False
		send(msg)
elif work == '0':
	loopstate = True
	while loopstate:	
		message_length = client.recv(64).decode('UTF-8')
		if message_length:
			message_length = int(message_length)
			ms = client.recv(message_length).decode('UTF-8')
			print(ms)
			if ms == 'cancel':
				loopstate = False
		



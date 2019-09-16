from socket import *
serverName="127.0.0.1"
serverPort=12000
serverSocket =socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName,serverPort))
serverSocket.listen(1)
print("Ready to receive")
while 1:
    ConnectionSocket,addr = serverSocket.accept()
    sentence = ConnectionSocket.recv(1024).decode()
    # print(sentence)
    file = open(sentence, "r")
    l = file. read(1024)
    ConnectionSocket.send( l. encode())
    file.close()
    ConnectionSocket.close()


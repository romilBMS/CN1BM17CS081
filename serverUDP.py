from socket import *
serverName="127.0.0.1"
serverPort=12000
serverSocket =socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName,serverPort))
# serverSocket.listen(1)
print("Ready to receive")
while 1:
    sentence,clientAddress = serverSocket.recvfrom(2048)
    # sentence = ConnectionSocket.recv(1024).decode()
    # print(sentence)
    file = open(sentence, "r")
    l = file. read(2048)
    serverSocket.sendto( bytes(l,"utf-8"), clientAddress)
    file.close()
    # ConnectionSocket.close()


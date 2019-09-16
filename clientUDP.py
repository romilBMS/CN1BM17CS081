from socket import *
serverName = "127.0.0.1"
serverPort=12000
clientSocket= socket(AF_INET, SOCK_DGRAM)
# clientSocket.connect((serverName, serverPort))
sentence = input("Enter file name")
clientSocket. sendto(bytes(sentence,"utf-8"), (serverName, serverPort))
fileContents, serverAddress= clientSocket. recvfrom(2048)
print("From server", fileContents)
clientSocket.close()
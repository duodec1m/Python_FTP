import socket

headerSize = 10

# keep sending data until all bytes are sent
def sendData(sock, data):
    data = data.encode("utf-8")
    sentBytes = 0
    while len(data) > sentBytes:
        sentBytes += sock.send(data[sentBytes:])

   
# keep receiving data until all bytes are received
def receiveData(sock, size):
    return sock.recv(size).decode("utf-8")
        
# make data size fit in fixed header size
def fixSize(data, size):
    data = str(data)
    while len(data) < size:
        data = "0" + data
    return data











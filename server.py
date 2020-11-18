import os, sys, socket
from resources import sendData, receiveData, fixSize, headerSize

serverDirectory = "./serverFiles/"

def push(cSocket):
    fileName = cSocket.recv(40) # name of file to get
    fileName = fileName.decode()

    try:
        fpath = os.path.join(serverDirectory, fileName) #get file
        fData = open(fpath)
        content = fData.read()
    except Exception as e:
        print(fileName + " does not exist")
        cSocket.send("-1".encode())
        return
    
    contentSize = str(len(content)).encode() # content length gets sent first
    cSocket.send(contentSize)
    
    while True:
        content = content.encode()
        cSocket.send(content)
        dataRecv = cSocket.recv(40)
        dataRecv = dataRecv.decode()
        if dataRecv == "done":
            print("Successfully sent file " + fileName)
            break
    return 0

def pull(cSocket):
    # create new socket for data transfer
    try:
        sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sSocket.bind(('', 0))
        sSocket.listen(1)
    except Exception as e:
        print("Failed bind to a port")
        print(e)
        sys.exit()  

    servPort = sSocket.getsockname()[1] # port number for client
    sendData(cSocket, str(servPort))

    # accept client connection
    print("Listening to port " + str(servPort))
    dataSocket, addr = sSocket.accept()
    print("Connected to address " + addr[0])

    # get name and data sizes
    fileNameSize = receiveData(dataSocket, headerSize)
    fileDataSize = receiveData(dataSocket, headerSize)

    # do not proceed if failed to get name and data sizes
    if fileNameSize == "":
        print("Failed to receive file name size")
        dataSocket.close()
        return
    if fileDataSize == "":
        print("Failed to receive file data size")
        dataSocket.close()
        return

    # read name and data
    fileName = receiveData(dataSocket, int(fileNameSize))
    fileData = receiveData(dataSocket, int(fileDataSize))

    # write file
    filePath = serverDirectory + fileName
    userFile = open(filePath, "w")
    userFile.write(fileData)
    userFile.close()
    fileSize = os.path.getsize(filePath)

    print(fileName + " received of file size " + str(fileSize) + " bytes")
    
    dataSocket.close()    

def run(args):
    if len(args) != 2:
        print("To run, please input command: python3 server.py <PORT>")
        sys.exit()

    port = args[1]

    # bind socket to a port
    try:
        sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sSocket.bind(('', int(port)))
        sSocket.listen(1)
    except Exception as e:
        print("Failed bind to a port")
        print(e)
        sys.exit()        

    while True:
        print("Listening to port " + port)
        cSocket, addr = sSocket.accept()
        print("Connected to address " + addr[0])

        while True:
            query = receiveData(cSocket, headerSize)

            if query == "get":
                push(cSocket)

            elif query == "put":
                pull(cSocket)

            elif query == "ls":
                files = os.listdir(serverDirectory) # get files
                response = ""
                for file in files:
                    response += file + "  "
                response = response[:-2]

                # send response
                responseSize = fixSize(len(response), headerSize)
                data = responseSize + response
                sendData(cSocket, data)

            elif query == "quit":
                cSocket.close()
                print("Connection closed")
                sys.exit(0)                
                break

            else:
                print("Received an invalid command")

if __name__ == '__main__':
    run(sys.argv)

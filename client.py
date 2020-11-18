import os, sys, socket
from resources import sendData, receiveData, fixSize, headerSize

clientDirectory = "./clientFiles/"

def get(cSocket, fileName):
    sendName = fileName.encode()
    cSocket.send(sendName)

    full_msg = "" # variable to hold incoming data
    contentSize = cSocket.recv(40) # content size
    if contentSize == b"-1": # file does not exist
        print(fileName + " does not exist on the server")
        return
    if contentSize != '0':
        contentSize = contentSize.decode()
        contentSize = int(contentSize)
        while len(full_msg)<contentSize:
                msg = cSocket.recv(40)
                full_msg += msg.decode()

    cSocket.send("done".encode())
    print(fileName + " received of file size " + str(contentSize) + " bytes")

    #Create and write to file
    fpath = os.path.join(clientDirectory, fileName)
    fData = open(fpath, "w")
    fData.write(full_msg)
    fData.close()

    return 0

def put(cSocket, server, fileName, userFile):
    dataPort = receiveData(cSocket, headerSize) #server port to transfer file

    # connect to new port
    try:
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.connect((server, int(dataPort)))
    except Exception as e:
        print("Failed to connect to server")
        print(e)
        return

    filePath = clientDirectory + fileName #path to file
    fileSize = os.path.getsize(filePath) # get file size
    
    # make file size and file name headers
    fileNameSize = fixSize(len(fileName), headerSize)
    fileDataSize = fixSize(fileSize, headerSize)
    fileData = userFile.read()
    
    data = fileNameSize + fileDataSize + fileName + fileData # headers

    # send data
    sendData(dataSocket, data)
    print( fileName + " successfully uploaded of size " + str(fileSize) + " bytes")

    userFile.close()
    dataSocket.close()
    print("Data transfer finish")


def run(args):
    if len(args) != 3:
        print("To run, please input command: python3 client.py <SERVER> <PORT>")
        sys.exit()

    server = args[1]
    port = args[2]

    # connect to server
    try:
        cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cSocket.connect((server, int(port)))
        print("Connected to " + server + " on port " + str(port))
    except Exception as e:
        print("Failed to connect to " + server)
        print(e)
        sys.exit()       

    query = "" # user input

    while True:
        query = (input("ftp> ")).lower().split()

        if query[0] == "get" and len(query) == 2:
            if len(query) != 2:
                print("To use get command: get <FILE NAME>")
            else:
                sendData(cSocket, query[0])
                get(cSocket, query[1])

        elif query[0] == "put" and len(query) == 2:
            if len(query) != 2:
                print("To use put command: put <FILE NAME>")
            else:
                try:
                    userFile = open(clientDirectory + query[1], "r")
                    sendData(cSocket, query[0])
                    put(cSocket, server, query[1], userFile)
                except Exception as e:
                    print(e)

        elif query[0] == "ls" and len(query) == 1:
            sendData(cSocket, query[0])
            responseSize = receiveData(cSocket, headerSize)

            if responseSize == "":
                print("Failed to receive size of response")
            else:
                response = receiveData(cSocket, int(responseSize))
                print(response)

        elif query[0] == "quit" and len(query) == 1:
            sendData(cSocket, query[0])
            cSocket.close()
            print("Connection closed")
            break
        
        else:
            print("Unknown command")


if __name__ == '__main__':
    run(sys.argv)

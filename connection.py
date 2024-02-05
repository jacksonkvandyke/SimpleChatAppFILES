import socket
import random
import threading
import time

#Connection class
class ConnectionClass:
    def __init__(self):
        self.hostObject = None
        self.socket = None
        self.port = None
        self.address = None
        self.connectedSocket = None
        self.connectedAddress = None
        self.inputBuffer = []
        self.outputBuffer = []

    def getPort(self):
        return self.port
    
    def getAddress(self):
        return self.address

    def getConnectedPort(self):
        return self.connectedSocket
    
    def getConnectedAddress(self):
        return self.connectedAddress
    
    #Close socket
    def closeSocket(self):
        if self.socket != None:
            self.socket.close()
    
    #This is for being the host
    def setConnection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind(("localhost", random.randrange(40000, 60000)))
        except:
            print("Socket creation was unsuccessful")
            return

        self.address, self.port = self.socket.getsockname()
        return
    
    def awaitConnection(self, hostObject):
        self.hostObject = hostObject
        connectionThread = threading.Thread(target=self.hostThread)
        connectionThread.start()

    def hostThread(self):
        self.socket.listen(1)
        self.connectedSocket, self.connectedAddress = self.socket.accept()
        self.hostObject.chatBox()
        self.transmitData()

    #This is for connecting to a host
    def getConnection(self, address, port, hostObject):
        self.hostObject = hostObject
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((address, int(port)))
        except:
            print("That connection does not exist or was unsuccessful.")
            return
        
        self.transmitData()

    #This is for data transfer
    def transmitData(self):
        inputThread = threading.Thread(target=self.inputThread)
        inputThread.start()

        outputThread = threading.Thread(target=self.outputThread)
        outputThread.start()

    def inputThread(self):
        while True:
            #Check if this is the host socket
            if self.connectedSocket == None:
                self.connectedSocket = self.socket
            
            inputString = ''
            inputString = self.connectedSocket.recv(1024)

            #Send input to UI
            self.inputBuffer = self.hostObject.getinputBuffer()
            self.inputBuffer.append(inputString)

            #Sleep to reduce strain on computer
            time.sleep(1)

    def outputThread(self):
        while True:
            outputString = ''
            self.outputBuffer = self.hostObject.getoutputBuffer()

            #Get the message from the output buffer
            if(len(self.outputBuffer) > 0):
                recievedString = self.outputBuffer[0]
                timeString = str(time.localtime().tm_mon) + "/" + str(time.localtime().tm_mday) + "/" + str(time.localtime().tm_year) + "-" + str(time.localtime().tm_hour % 12) + ":" + str(time.localtime().tm_min)
                outputString = timeString + " |Incoming| " + recievedString + "\n"
                self.outputBuffer.remove(recievedString)
                print("In buffer")

            #Send data
            dataLength = len(outputString)
            sent = 0
            while(sent < dataLength):
                sent += self.connectedSocket.send(outputString.encode())
                print("Sent")

            #Sleep to reduce strain on computer
            time.sleep(1)

from tkinter import *
import threading
import connection
import time

class UIClass:

    def __init__(self):
        self.window = None
        self.frame = None
        self.uiElements = [] 
        self.inputBuffer = []
        self.outputBuffer = []
        self.socket = None

    #Create window 
    def createWindow(self):
        self.window = Tk()
        self.frame = Frame(self.window)
        self.window.config(height=500, width=500)
        self.window.title("Simple Chat App")
        self.createHomescreen()

        mainloop()

        #Close local and external socket
        if self.socket != None:
            self.socket.connectedSocket.close()
            self.socket.closeSocket()

        return

    #Create homescreen
    def createHomescreen(self):
        l1 = Label(self.window, text="Simple Chat", font=("Ariel", 30))
        b1 = Button(self.window, text="Host", font=("Ariel", 16), command=self.hostConnection)
        b2 = Button(self.window, text="Connect", font=("Ariel", 16), command=self.connectionWindow)

        l1.grid(column=0, row=0)
        b1.grid(column=0, row=1)
        b2.grid(column=0, row=2)

        self.uiElements.append(l1)
        self.uiElements.append(b1)
        self.uiElements.append(b2)

    #Host Connection
    def hostConnection(self):
        self.socket = connection.ConnectionClass()
        self.socket.setConnection()

        #Remove previous UI
        for element in self.uiElements:
            element.grid_remove()
        self.uiElements.clear()
    
        #Add new UI
        l1 = Label(self.window, text="Simple Chat", font=("Ariel", 30))
        l2 = Label(self.window, text="You are currently hosting a connection. Please wait for another instance to connect.", font=("Ariel", 16))
        l3 = Label(self.window, text="Port: %s" % (self.socket.getPort()), font=("Ariel", 16))
        l4 = Label(self.window, text="Address: %s" % (self.socket.getAddress()), font=("Ariel", 16))

        l1.grid(column=0, row=0)
        l2.grid(column=0, row=1)
        l3.grid(column=0, row=2)
        l4.grid(column=0, row=3)

        self.uiElements.append(l1)
        self.uiElements.append(l2)
        self.uiElements.append(l3)
        self.uiElements.append(l4)

        #Await connection
        self.socket.awaitConnection(self)

    def connectionWindow(self):
        #Remove previous UI
        for element in self.uiElements:
            element.grid_remove()
        self.uiElements.clear()
    
        #Add new UI and required variables
        address = StringVar()
        port = StringVar()
        l1 = Label(self.window, text="Simple Chat", font=("Ariel", 30))
        l2 = Label(self.window, text="Please enter the connection info.", font=("Ariel", 16))
        l3 = Label(self.window, text="Port: ", font=("Ariel", 12))
        l4 = Label(self.window, text="Address: ", font=("Ariel", 12))
        e1 = Entry(self.window, font=("Ariel", 16), textvariable=port)
        e2 = Entry(self.window, font=("Ariel", 16), textvariable=address)
        b1 = Button(self.window, text="Connect", font=("Ariel", 12), command=lambda: self.connectTo(address.get(), port.get()))

        l1.grid(column=0, row=0)
        l2.grid(column=0, row=1)
        l3.grid(column=0, row=2)
        l4.grid(column=0, row=5)
        e1.grid(column=0, row=4)
        e2.grid(column=0, row=6)
        b1.grid(column=0, row=7)

        self.uiElements.append(l1)
        self.uiElements.append(l2)
        self.uiElements.append(l3)
        self.uiElements.append(l4)
        self.uiElements.append(e1)
        self.uiElements.append(e2)
        self.uiElements.append(b1)

    def connectTo(self, address, port):
        self.socket = connection.ConnectionClass()
        self.socket.getConnection(address, port, self)
        self.chatBox()

    def chatBox(self):
        #Remove previous UI
        for element in self.uiElements:
            element.grid_remove()
        self.uiElements.clear()

        #Create outputstring variable
        outputString = StringVar()

        #Add new UI
        l1 = Label(self.window, text="Simple Chat", font=("Ariel", 30))
        s1 = Scrollbar(self.window, orient='vertical')
        t1 = Text(self.window, wrap=WORD, width=40, height=5, font=("Arial", 15))
        e1 = Entry(self.window, width=40, font=("Ariel", 15), textvariable=outputString)
        b1 = Button(self.window, text="Send", font=("Ariel", 15), command=lambda: self.sendMessage(outputString, t1))

        l1.grid(column=0, row=0)
        s1.grid(column=1, row=1, sticky="ns", pady=0)
        t1.grid(column=0, row=1)
        e1.grid(column=0, row=2)
        b1.grid(column=1, row=2)

        #Connect listbox to scrollbar
        t1.config(yscrollcommand=s1.set)
        s1.config(command=t1.yview)

        #Create chatBox thread and configure tags
        t1.tag_config("grey", foreground='grey')
        updateThread = threading.Thread(target=self.updateBox, args=[t1])
        updateThread.start()

    def sendMessage(self, outputString, box):
        #Get text entry
        text = outputString.get()
        self.outputBuffer.append(text)
        outputString.set('')

        #Add text to sent messages
        timeString = str(time.localtime().tm_mon) + "/" + str(time.localtime().tm_mday) + "/" + str(time.localtime().tm_year) + "-" + str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min)
        sentMessage = timeString + " |Outgoing| " + text + "\n"
        box['state'] = NORMAL
        box.insert(END, sentMessage, 'grey')
        box['state'] = DISABLED

    def updateBox(self, box):
        while True:
            #Loop through inputBuffer
            for message in self.inputBuffer:
                box['state'] = NORMAL
                box.insert(END, message)
                self.inputBuffer.remove(message)

            #Sleep to reduce strain on computer
            box['state'] = DISABLED
            time.sleep(1)
        
    def getinputBuffer(self):
        return self.inputBuffer
    
    def getoutputBuffer(self):
        return self.outputBuffer
        
        
    
newApp = UIClass()
newApp.createWindow()

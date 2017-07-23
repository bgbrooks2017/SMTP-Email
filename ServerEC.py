from socket import *
import sys

#receive and respond to the HELO command
def recvHelo():
    helo = connectionSocket.recv(1024)
    if helo[:4] =="HELO":
        ACK = "250 " + helo + " pleased to meet you."
        connectionSocket.send(ACK)


#receive and respond to the SMTP commands from the user/client
def recvMFC():
    global MFC
    MFC = connectionSocket.recv(1024)
    ACK = "250 OK MFC ACK"
    connectionSocket.send(ACK)

def recvRCPT():
    global RCPTlist
    RCPTlist=[]
    while True:
        RCPT = connectionSocket.recv(1024)
        if RCPT[:4]=="DATA":
            break
        RCPTlist.append(RCPT)
        ACK = "250 OK RCPT ACK"
        connectionSocket.send(ACK)

def recvDATA():
    ACK = "354 enter your message"
    connectionSocket.send(ACK)

def recvDataMsg():
    global dataMsg
    dataMsg = connectionSocket.recv(8000)

def recvDot():
    dot = connectionSocket.recv(1024)
    if dot ==".\n":
        ACK = "250 OK DOT ACK"
        connectionSocket.send(ACK)

def recvQUIT():
    quit = connectionSocket.recv(1024)
    if quit[:4]=="QUIT":
        connectionSocket.close()


def sendToFile():
    #get the mailbox to send to
    counter = 0
    while RCPTlist[0][counter]!="@":
        counter = counter + 1
        domStart = counter+1
    while RCPTlist[0][counter]!=">":
        counter = counter + 1
        domEnd = counter
    dom = RCPTlist[0][domStart:domEnd]


    #build my file to send
    forwardFile = []
    forwardFile.append(MFC)
    for count in RCPTlist:
        forwardFile.append(count)
    forwardFile.append(dataMsg)
    #open and write to file
    f = open('forward/' + dom, 'a+')
    for g in forwardFile:
        f.write(g +'\n')




try:
    serverPort = int(sys.argv[1])
    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverSocket.bind(('',serverPort))

    serverSocket.listen(1)
    while True:
        connectionSocket, clientAddress = serverSocket.accept()
        connectionSocket.send("220 " + gethostname())
        recvHelo()
        recvMFC()
        recvRCPT()
        recvDATA()
        recvDataMsg()
        recvDot()
        recvQUIT()
        sendToFile()

        connectionSocket.close()
except error:
    print "There was an issue with the connection to the socket -- terminating program"

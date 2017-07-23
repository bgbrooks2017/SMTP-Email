from socket import *
import sys
import base64




global errpath
errpath = False
global errdom
errdom = False


#check for errors in the path/domain
def printErr(errpath, errdom):
    if errpath == True and errdom ==True:
        print "Error in path"
    if errpath == False and errdom == True:
        print "Error in domain"
    if errpath == True and errdom ==False:
        print "Error in path"
    if errpath == False and errdom == False:
        pass

#check domain
def checkDomain(path, count):
    try:
        startdom = count
        domChar = False
        global errdom
        if path[count].isalpha():

            count = count+1
            domChar = True
        else:
            errdom = True
        while path[count].isalnum():
            count = count+1
        if path[count] =="." and path[count-1] ==".":
            errdom = True
        if path[count] == ".":
            enddom = count
            twoCheck = enddom-startdom
            if twoCheck<2:
                errdom = True
            count = count +1
            checkDomain(path, count)
    except IndexError:
        if path[count-1]==".":
            errdom = True

#check path
def checkPath(path):

    try:
        count = 0
        global errpath
        while path[count] not in "<>()[]\.,;:@\"":
            if path[count].isspace():
                errpath = True
            count = count + 1
            char = True
        if path[count] == "@" and char == True:
            count = count+1
            checkDomain(path, count)
        else:
            errpath = True

    except IndexError:
        errpath = True












#From: prompt.
def fromPrompt():
    global errpath
    global errdom
    errpath = False
    errdom = False
    sender = raw_input("From:")
    global fromPath
    fromPath = sender.strip()
    checkPath(fromPath)
    printErr(errpath, errdom)
    if errpath == True or errdom == True:
        fromPrompt()





#To: prompt
def toPrompt():
    global errpath
    errpath = False
    global errdom
    errdom = False
    global recipientList
    recipientList = []
    del recipientList[:]
    recipients = raw_input("To:")
    recipientList = recipients.split(",")
    counter= 0
    while counter< len(recipientList):
        toPath = recipientList[counter].strip()
        checkPath(toPath)
        printErr(errpath, errdom)
        if errpath == True or errdom == True:
            toPrompt()
        counter = counter+1

#Subject prompt
def subjectPrompt():
    global subject
    subject = raw_input("Subject:")

#Message: prompt
def messagePrompt():
    line = ""
    global text
    text = ""
    print("Message:")
    message = []
    while line!=".":
        line=raw_input()
        message.append(line)
        counter= 0

    while counter< len(message) - 1:
        text = text + message[counter] + '\n'
        counter= counter+ 1
def attatchPrompt():
    jpeg = raw_input("Attatchment:")
    with open(jpeg, "rb") as image_file:
        global encoded_string
        encoded_string = base64.b64encode(image_file.read())



def socketProg():
    try:
        serverName = sys.argv[1]
        serverPort = int(sys.argv[2])
        global clientSocket
        clientSocket= socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        greeting = clientSocket.recv(128)
        if greeting[:3]!="220":
            print "greeting ACK not received"
            clientSocket.close()
            quit()



        domName = "HELO " + getfqdn() +'\n'
        clientSocket.send(domName)
        heloACK = clientSocket.recv(128)
        if heloACK[:3]!="250":
            print "HELO ACK not received"
            clientSocket.close()
            quit()


        sendMFC()
        sendRCPT()
        sendDATA()
        sendDataMsg()
        sendDot()
        sendQuit()
    except error:
        print "Socket error -- program needed to terminate"
        clientSocket.close()

#send Mail FROM TO server
def sendMFC():

    mfcName = "MAIL FROM: " + "<" +fromPath + ">" +'\n'
    clientSocket.send(mfcName)
    mfcACK = clientSocket.recv(128)
    if mfcACK[:3]!="250":
        print "MFC ACK not received"
        clientSocket.close()
        quit()

def sendRCPT():
    counter = 0
    while counter < len(recipientList):
        rcptName = "RCPT TO: " + "<" + recipientList[counter].strip() + ">" + '\n'
        clientSocket.send(rcptName)
        rcptACK = clientSocket.recv(128)
        if rcptACK[:3]!="250":
            print "RCPT ACK not received"
            clientSocket.close()
            quit()
        counter = counter + 1

def sendDATA():
    clientSocket.send("DATA\n")
    DataACK = clientSocket.recv(128)
    if DataACK[:3]!="354":
        print "DATA ACK not received"
        clientSocket.close()
        quit()

def sendDataMsg():
    dataMsg ="From: "+fromPath +'\n'
    counter = 0
    rcptName =[]
    while counter<len(recipientList):
        rcptName = recipientList[counter].strip()
        dataMsg = dataMsg + "To: "  + rcptName  + '\n'
        counter = counter + 1

    dataMsg = dataMsg + "Subject: " + subject +'\n'
    dataMsg = dataMsg + "MIME-Version: 1.0" + '\n'
    dataMsg = dataMsg + "Content-Type: multipart/mixed; boundary=987654321" + '\n' + '\n'
    dataMsg = dataMsg +  "--987654321" + '\n'
    dataMsg = dataMsg + "Content-Transfer-Encoding: quoted-printable" +'\n'
    dataMsg = dataMsg + "Content-Type: text/plain; charset=us-ascii" +'\n' + '\n'
    dataMsg = dataMsg + text +'\n'
    dataMsg = dataMsg + "--987654321" +'\n'
    dataMsg = dataMsg + "Content-Transfer-Encoding: base64" +'\n'
    dataMsg = dataMsg + "Content-Type: image/jpeg" +'\n' +'\n'
    dataMsg = dataMsg + encoded_string + '\n'
    dataMsg = dataMsg + "--987654321" +'\n'
    clientSocket.send(dataMsg)

def sendDot():
    clientSocket.send("." + '\n')
    dotACK = clientSocket.recv(128)
    if dotACK[:3]!="250":
        print "DOT ACK not received"
        clientSocket.close()
        quit()

def sendQuit():
    clientSocket.send("QUIT")



def main():
    try:
        fromPrompt()
        toPrompt()
        subjectPrompt()
        messagePrompt()
        attatchPrompt()
    except EOFError:
        print "\n client terminated without sending a complete message to the server -- Please try again"
        quit()
    socketProg()





if __name__ =='__main__':
    main()

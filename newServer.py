import argparse
from email import message
import socket
import struct

#Setting command line arguments
parser = argparse.ArgumentParser(description='Message.')

parser.add_argument('-p', type=str, required=True)
parser.add_argument('-l', type=str, required=True)
args = parser.parse_args()

port= int(args.p)
logFile = args.l

s = struct.Struct("> III")

#Checking for valid port
if((int(port)) < 0 or (int(port)) > 65535) :
    print("Error invalid port, try agian with a different port number.")
    exit()

#Creating Socket
while True: 
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.inet_aton("127.0.0.1")

    try:
        serversocket.bind(("127.0.0.1", port))

    except: 
        print("Error, did not bind. Try again with a different port number")
        
    serversocket.listen(5)
    conn, address = serversocket.accept()

    file = open(logFile, "a")

    #Receiving Data from client
    header = conn.recv(struct.calcsize('>III'))
    version, msg_type, msg_len = struct.unpack('>III', header)
    data = conn.recv(msg_len)

    #Acknowledgement 
    if(data.decode()=="HELLO"):

        file.write("Received connection from (IP, PORT):" + str(port))
        print("Received connection from (IP, PORT):" + str(port))

        version= 17
        msg_type = 0
        message = "HELLO".encode()
        msg_len = len("HELLO")
        header = s.pack(version, msg_type, msg_len)

        conn.send(header)
        conn.sendall(message)

    #Printing data that is recieved
    print(f"Received Data: version: {version} message_type:  {msg_type} length: {msg_len}")
    file.write(f"Received Data: version: {version} message_type:  {msg_type} length: {msg_len}")

    #Checking for valid version
    if(version==17):
        print("VERSION ACCEPTED")
        file.write("VERSION ACCEPTED")

        header = conn.recv(struct.calcsize('>III'))
        version, msg_type, msg_len = struct.unpack('>III', header)

        if(msg_type==1):
            print("EXECUTING SUPPORTED COMMAND: LIGHTON")
            file.write("EXECUTING SUPPORTED COMMAND: LIGHTON")

            print("Returning Success")
            file.write("Returning Success")

            successMessage = "Success".encode()
            conn.sendall(successMessage)

        elif(msg_type==2):
            print("EXECUTING SUPPORTED COMMAND: LIGHTOFF")
            file.write("EXECUTING SUPPORTED COMMAND: LIGHTOFF")

            print("Returning Success")
            file.write("Returning Success")

            successMessage = "Success".encode()
            conn.sendall(successMessage)
        
        elif(msg_type==3):
            print("EXECUTING SUPPORTED COMMAND: DISCONNECT")
            file.write("EXECUTING SUPPORTED COMMAND: DISCONNECT")

            print("Returning Success")
            file.write("Returning Success")

            successMessage = "Success".encode()
            conn.sendall(successMessage)

    else:
        print("VERSION MISMATCH")
        file.write("VERSION MISMATCH")

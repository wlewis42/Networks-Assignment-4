import argparse
from _thread import *
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
    print("\nError invalid port, try agian with a different port number.")
    exit()

def threaded_client(connection):
        file = open(logFile, "a")

        #Receiving Data from client
        header = connection.recv(struct.calcsize('>III'))
        version, msg_type, msg_len = struct.unpack('>III', header)
        data = connection.recv(msg_len)

        #Acknowledgement 
        if(data.decode()=="HELLO"):

            file.write(f"\nReceived connection from (IP, PORT): {address}")
            # print("Received connection from (IP, PORT):" + str(port))
            print(f"\nReceived connection from (IP, PORT): {address}")

            version= 17
            msg_type = 0
            message = "HELLO".encode()
            msg_len = len("HELLO")
            header = s.pack(version, msg_type, msg_len)

            connection.send(header)
            connection.sendall(message)

        #Printing data that is recieved
        print(f"\nReceived Data: version: {version} message_type:  {msg_type} length: {msg_len}")
        file.write(f"\nReceived Data: version: {version} message_type:  {msg_type} length: {msg_len}\n")

        #Checking for valid version
        if(version==17):
            print("\nVERSION ACCEPTED")
            file.write("\nVERSION ACCEPTED")

            header = connection.recv(struct.calcsize('>III'))
            version, msg_type, msg_len = struct.unpack('>III', header)

            if(msg_type==1):
                print("\nEXECUTING SUPPORTED COMMAND: LIGHTON")
                file.write("\nEXECUTING SUPPORTED COMMAND: LIGHTON")

                print("\nReturning Success")
                file.write("\nReturning Success")

                successMessage = "Success".encode()
                connection.sendall(successMessage)

            elif(msg_type==2):
                print("\nEXECUTING SUPPORTED COMMAND: LIGHTOFF")
                file.write("\nEXECUTING SUPPORTED COMMAND: LIGHTOFF")

                print("\nReturning Success")
                file.write("\nReturning Success")

                successMessage = "Success".encode()
                connection.sendall(successMessage)
            
            elif(msg_type==3):
                print("\nEXECUTING SUPPORTED COMMAND: DISCONNECT")
                file.write("\nEXECUTING SUPPORTED COMMAND: DISCONNECT")

                print("\nReturning Success")
                file.write("\nReturning Success")

                successMessage = "Success".encode()
                connection.sendall(successMessage)

        else:
            print("\nVERSION MISMATCH")
            file.write("\nVERSION MISMATCH")

#Creating Socket
while True: 
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.inet_aton("127.0.0.1")

    try:
        serversocket.bind(("127.0.0.1", port))

    except: 
        print("\nError, did not bind. Try again with a different port number")
        
    serversocket.listen(5)
    conn, address = serversocket.accept()
    start_new_thread(threaded_client, (conn,))

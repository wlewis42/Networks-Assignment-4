import argparse
from _thread import *
import socket
import struct

'''
Parse port and logfile arguments
'''
parser = argparse.ArgumentParser(description='Message.')

parser.add_argument('-p', type=str, required=True)
parser.add_argument('-l', type=str, required=True)
args = parser.parse_args()

port= int(args.p)
logFile = args.l

s = struct.Struct("> III")

'''
Validate port number is within proper range
'''
if((int(port)) < 0 or (int(port)) > 65535) :
    print("Error: Invalid port.\n")
    exit()

'''
Define function for threaded client
    arguements: connection
    returns: none
'''
def threaded_client(connection):
        '''
        Open logfile in append mode
        '''
        file = open(logFile, "a")

        '''
        Receive header and data
        '''
        header = connection.recv(struct.calcsize('>III'))
        version, msg_type, msg_len = struct.unpack('>III', header)
        data = connection.recv(msg_len)

        '''
        Three-way handshake 
        '''
        if(data.decode()=="HELLO"):
            '''
            IF client sent HELLO, reply with HELLO
            '''
            file.write(f"Received connection from (IP, PORT): {address}\n")
            print(f"Received connection from (IP, PORT): {address}\n")
            version= 17
            msg_type = 0
            msg = "HELLO".encode()
            msg_len = len("HELLO")
            header = s.pack(version, msg_type, msg_len)
            connection.send(header)
            connection.sendall(msg)

        '''
        Log message data from header
        '''
        print(f"Received Data: version: {version} message_type:  {msg_type} length: {msg_len}\n")
        file.write(f"Received Data: version: {version} message_type:  {msg_type} length: {msg_len}\n")

        '''
        Check for valid version number
        '''
        if(version==17):
            print("VERSION ACCEPTED\n")
            file.write("VERSION ACCEPTED\n")

            '''
            Receive message from client
            '''
            header = connection.recv(struct.calcsize('>III'))
            version, msg_type, msg_len = struct.unpack('>III', header)

            '''
            Check for message type
            '''
            successMessage = "Success".encode()
            if(msg_type==1):
                print("EXECUTING SUPPORTED COMMAND: LIGHTON\n")
                print("Returning Success\n")
                file.write("EXECUTING SUPPORTED COMMAND: LIGHTON\n")
                file.write("Returning Success\n")
                connection.sendall(successMessage)

            elif(msg_type==2):
                print("EXECUTING SUPPORTED COMMAND: LIGHTOFF\n")
                print("Returning Success\n")
                file.write("EXECUTING SUPPORTED COMMAND: LIGHTOFF\n")
                file.write("Returning Success\n")
                connection.sendall(successMessage)
            
            elif(msg_type==3):
                print("EXECUTING SUPPORTED COMMAND: DISCONNECT\n")
                print("Returning Success\n")
                file.write("EXECUTING SUPPORTED COMMAND: DISCONNECT\n")
                file.write("Returning Success\n")
                connection.sendall(successMessage)

        else:
            print("VERSION MISMATCH\n")
            file.write("VERSION MISMATCH\n")

'''
Handle incoming connections
'''
while True: 
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.inet_aton("127.0.0.1")

    try:
        serversocket.bind(("127.0.0.1", port))    

    except: 
        print("ERROR: Unable to bind with that IP, PORT combination\n")
    
    serversocket.listen(5)
    conn, address = serversocket.accept()
    start_new_thread(threaded_client, (conn,))

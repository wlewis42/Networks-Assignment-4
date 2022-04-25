
# takes four arguements
# anonclient -s <LOAD-BALANCER-IP> -p <PORT> -l LOGFILE -f <file_to_write_to>

# The client will simply open a connection to the load-balancer and request a content
# Recieve content and write to a file

import argparse
from email import message
import socket
import struct

#Setting command line arguments
parser = argparse.ArgumentParser(description='Connecting... ')

parser.add_argument("-s", type=str, required=True)
parser.add_argument("-p", type=str, required=True)
parser.add_argument("-l", type=str, required=True)
parser.add_argument("-f", type=str, required=True)

args = parser.parse_args()

ip = args.s
port= int(args.p)
logFile = args.l
writeFile = args.f

if((int(port)) < 0 or (int(port)) > 65535) :
    print("Error invalid port, try agian with a different port number.")
    exit()

while True:
    # Create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Open logFile
    file = open(logFile, "a")

    # Connect
    client.connect((ip, port)) 
    s = struct.Struct("> sI")

    header = client.recv(struct.calcsize('>sI'))
    mess, msg_len = struct.unpack('>sI', header)

    # Receive best IP
    print("\nReceived Data: " + str(mess))
    file.write("Received Data: " + str(mess) + "\n")

    # Close socket after finding best IP
    client.close()

    # Open Another connection with replica sever
    # !!!!!!!!!! May have to add port !!!!!!!!!!!!
    client.connect((mess,)) 

    header = client.recv(struct.calcsize('>sI'))
    r, len = struct.unpack('>sI', header)

    replicaFile = open(writeFile, "a")

    file.write("\nReceived Data: " + r)
    replicaFile.write(r)






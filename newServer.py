import argparse
import struct
import socket

ServerSocket = socket.socket()

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port",
                    help="The port server listens on", 
                    type=str)
parser.add_argument("-l", "--logfile",
                    help="Where you will keep a record of actions", 
                    type=str)
args = parser.parse_args()

host = '127.0.0.1'
port = int(args.port)
logfile = args.logfile

while True:
   try:
      ServerSocket.bind((host, port))
      ServerSocket.listen(5)
   except socket.error as e:
      print(str(e))
   try:
      client, address = ServerSocket.accept()
      print(f"Received connection from {address}, {client}")
   except:
      print("An error in connecting occurred")
   
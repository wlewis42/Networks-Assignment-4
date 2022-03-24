import socket
import argparse
from _thread import *
import struct
import binascii


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
ThreadCount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

# 1 listen for connections on specified port
ServerSocket.listen(5)

# create header based on message argument
def send(message, connection):
   version = 17
   if message=="HELLO":
      msg_type = 0
      msg_len = len(message)
   if message=="LIGHTON":
      msg_type = 1
      msg_len = len(message)
   if message=="LIGHTOFF":
      msg_type = 2
      msg_len = len(message)
   if message=="DISCONNECT":
      msg_type = 3
      msg_len = len(message)
   # create header with struct
   values = (version, msg_type, msg_len)
   s=struct.Struct('>III')
   # pack header
   packed_data = s.pack(*values)
   # send header
   connection.sendall(packed_data)

"""
Checks for correct version, logs message, and returns boolean
"""
def isCorrectVersion(version):
   log = open(logfile, "a")
   if version == 17:
      log.write("Version Accepted")
      return True
   else:
      log.write("Version Miscmatch")
      return False

"""
Receive data from the client and log the data

:param connection: The socket object that is being used to send and receive data
"""
def threaded_client(connection):
   log = open(logfile, "a")
   while True:
      # receive header
      version,msg_type,msg_len = connection.recv(struct.calcsize(">III"))
      log.write(f"Received Data: version: {version} message_type: {msg_type} length: {msg_len}")
      # log.close()
      # check version
      if (isCorrectVersion(version)):

         data = connection.recv(msg_len)
         if not data:
            break
   connection.close()

while True:
   Client, address = ServerSocket.accept()
   rec_conn = (f"Received connection from (IP, PORT): ('{address}',{Client})")
   print(rec_conn)
   # print('Connected to: ' + address[0] + ':' + str(address[1]))
   start_new_thread(threaded_client, (Client, ))
   ThreadCount += 1
   print('Thread Number: ' + str(ThreadCount))
# ServerSocket.close()

import argparse
from ipaddress import ip_address
import socket
import struct

'''
Parse server IP address, port number, and logfile and set
those values
'''
parser = argparse.ArgumentParser(description='Connecting to server')

parser.add_argument("-s", type=str, required=True)
parser.add_argument("-p", type=str, required=True)
parser.add_argument("-l", type=str, required=True)
parser.add_argument("-f", type=str, required=True)
args = parser.parse_args()

ip = args.s
port= int(args.p)
logFile = args.l
contentfile = args.f

# connect to load balancer
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ip, port))

# send request to load balancer
def sendCommand(command):
   s = struct.Struct("> III")

   with open(logFile, "a") as f:
      print(f"Message type: {msg_type}\t Command: {command}\n")
      f.write(f"Message type: {msg_type}\t Command: {command}\n")
      version = 17
      msg_type = 0
      com = command.encode()
      msg_len = len(command)
      header = s.pack(version, msg_type, msg_len)

      print(f"Sending {command} packet\n")
      f.write(f"Sending {command} packet\n")
      clientsocket.send(header)
      clientsocket.sendall(com)

# receive ip of best replica server from loadbalancer
'''
Receive and unpack data
'''
with open(logFile, 'a') as f:
   header = clientsocket.recv(struct.calcsize('>III'))
   version, msg_type, msg_len = struct.unpack('>III', header)
   server_ip = clientsocket.recv(msg_len) 

   print(f"Received connection from (IP, PORT): {ip}, {port}\n")
   f.write(f"Received connection from (IP, PORT): {ip}, {port}\n")
   print(f"Preferred Replica Server Address: {server_ip}\n")
   f.write(f"Preferred Replica Server Address: {server_ip}\n")
   # close connection to loadbalancer
   clientsocket.close()

   # connect to replica server
   print(f"Attemping Connection to {server_ip}\n")
   f.write(f"Attemping Connection to {server_ip}\n")

# connect to replica server
clientsocket.connect((server_ip,port))

sendCommand("REQUEST FILE")

# receive contentfile
req_head = clientsocket.recv(struct.calcsize('>III'))
req_ver, req_type, req_len = struct.unpack('>III', req_head)
req_data = clientsocket.recv(req_len)

# decode and write to file
with open(contentfile,'w') as f:
   f.write(req_data.decode())
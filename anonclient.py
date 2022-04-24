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
      f.write()
      version= 17
      msg_type = 0
      com = command.encode()
      msg_len = len(command)
      header = s.pack(version, msg_type, msg_len)

      f.write(f"Sending {command} packet\n")
      clientsocket.send(header)
      clientsocket.sendall(com)

sendCommand('HELLO')
# receive ip of best replica server

# connect to replica server

# receive contentfile
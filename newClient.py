import argparse
import socket
import struct


parser = argparse.ArgumentParser(description='Connect to a server')
parser.add_argument("-s", type=str, required=True)
parser.add_argument("-p", type=str, required=True)
parser.add_argument("-l", type=str, required=True)

# parse command line arguments
args = parser.parse_args()

# set important variables
ip = args.s
logfile = args.l

# check ip address validity
socket.inet_aton(ip)

# check port number validity
if((int(args.p)) > 0 or (int(args.p)) <= 65535):
   port = int(args.p)
else:
   print("Not a valid port number.")
   exit()

# user_input = input("Enter a command: ")

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect
try: 
   client_socket.connect(ip,port)
except:
   print(f"Could not connect using ip: {ip}, port: {port}")
# create struct
s = struct.Struct("> I I I")

# send commands
def sendHello():
   version= 17
   msg_type = 0
   msg_len = len("HELLO")
   header = (version, msg_type, msg_len)
   packed = s.pack(*header)
   client_socket.sendall(packed)
   client_socket.sendall("HELLO")

def sendLightOn():
   version= 17
   msg_type = 1
   msg_len = len("LIGHTON")
   header = (version, msg_type, msg_len)
   packed = struct.pack(*header)
   client_socket.sendall(packed)
   client_socket.sendall("LIGHTON")

def sendLightOff():
   version= 17
   msg_type = 2
   msg_len = len("LIGHTOFF")
   header = (version, msg_type, msg_len)
   packed = struct.pack(*header)
   client_socket.sendall(packed)
   client_socket.sendall("LIGHTOFF")

def sendGoodbye():
   version= 17
   msg_type = 3
   msg_len = len("DISCONNECT")
   header = (version, msg_type, msg_len)
   packed = struct.pack(*header)
   client_socket.sendall(packed)
   client_socket.sendall("DISCONNECT")

# receive messages
def receive():
   header = client_socket.recv(struct.calcsize('>III'))
   version, msg_type, msg_len = struct.unpack('>III', header)
   data = client_socket.recv(msg_len) # receive data
while True:
   user_input = input("Enter a comand: ")
   # send correct command
   if (user_input=="HELLO"):
      sendHello()
   elif (user_input=="LIGHTON"):
      sendLightOn()
   elif (user_input=="LIGHTOFF"):
      sendLightOff()
   elif (user_input=="DISCONNECT"):
      sendGoodbye()

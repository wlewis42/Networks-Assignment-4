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

user_input = input("Enter a command: ")

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect
try:
   client_socket.connect(ip,port)
except:
   print(f"Unable to connect to (IP, PORT): {ip}, {port}")
   log = open(logfile,"a")
   log.write(f"Unable to connect to (IP, PORT): {ip}, {port}")

try:
   client_socket.sendmsg("HELLO")
except:
   print(f"Unable to send 'HELLO'")

# send commands
def sendMsg(msg):
   log = open(logfile,"a")
   s = struct.Struct(">III"+msg.encode())
   version= 17
   if msg=='HELLO':
      msg_type = 0
   elif msg=='LIGHTON':
      msg_type = 1
   elif msg=='LIGHTOFF':
      msg_type = 2
   elif msg=='DISCONNECT':
      msg_type = 3
   msg_len = len(msg)
   header = (version, msg_type, msg_len, msg.encode())
   packed = s.pack(header)
   client_socket.sendall(packed)
   log.write(f"Sending Command {msg}")

# # receive messages
# def receive(data):
conn, addr = client_socket.accept()
print(f"Received Connection (IP, PORT): {addr}, {conn}")
header = conn.recv(struct.calcsize('>III'))
version, msg_type, msg_len = struct.unpack('>III',header)
msg = client_socket.recv(msg_len).decode() # receive data

# send correct command
if (user_input=="HELLO"):
   sendMsg(user_input)
elif (user_input=="LIGHTON"):
   sendMsg(user_input)
elif (user_input=="LIGHTOFF"):
   sendMsg(user_input)
elif (user_input=="DISCONNECT"):
   sendMsg(user_input)

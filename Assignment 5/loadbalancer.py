import argparse
import subprocess
# from http import server
# # import os
import struct
import socket

parser = argparse.ArgumentParser(description='Message.')

parser.add_argument('-s', type=str, required=True)
parser.add_argument('-p', type=str, required=True)
parser.add_argument('-l', type=str, required=True)
args = parser.parse_args()

server_ips = args.s
port= int(args.p)
log_file = args.l

'''
HEADER AND PACKET CREATION
'''
s = struct.Struct("> III")
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.bind((socket.gethostname(),port))
client_sock.listen(5)
clientsocket,address= client_sock.accept()

#Receive header and data        
header = client_sock.recv(struct.calcsize('>III'))
version, msg_type, msg_len = struct.unpack('>III', header)
data = client_sock.recv(msg_len)

replica_array = []

# Returns index of server with best preference
def getPreference(replica_servers_file):
   with open(replica_servers_file, 'r') as f:
      for line in f:
         replica_array.append(line)
   preference_array = []
   
   with open(log_file, 'a') as f:
      for ip in replica_array:
         print(f"Pinging {ip} from '{server_ips}'...\n")
         f.write(f"Pinging {ip} from '{server_ips}'...\n")
         pinged = subprocess.run(["ping", ip, "-n", "3"], capture_output=True, text=True).stdout.split()

         lossPercent = float(pinged[-17].split('(')[1].split('%')[0])
         delay = float(pinged[-4].split('ms,')[0])
         preference = (0.75*lossPercent) + (0.25*delay)
         print(f"Replica server at {ip}:\n\tLoss: {lossPercent}\tDelay: {delay}\tPreference: {preference}\n")
         f.write(f"Replica server at {ip}:\n\tLoss: {lossPercent}\tDelay: {delay}\tPreference: {preference}\n")
         preference_array.append(preference)
   
   return preference_array.index(min(preference_array))

# get replica with best preference
best_server = getPreference(server_ips)
# print(replica_array)
with open(log_file, 'a') as f:
   print(f"Connecting to {replica_array[best_server]} ...\n")
   f.write(f"Connecting to {replica_array[best_server]} ...\n")

# create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(socket.gethostname(),port)
serversocket.listen(5)

# Listen for incoming connection from client
while True:
   (clientsocket,address)=serversocket.accept()

   # create header, message, and packet
   version= 17
   msg_type = 1
   msg = best_server.encode()
   msg_len = len(best_server)
   header = s.pack(version, msg_type, msg_len)
   
   # send server ip address to client
   clientsocket.send(header)
   clientsocket.sendall(msg)

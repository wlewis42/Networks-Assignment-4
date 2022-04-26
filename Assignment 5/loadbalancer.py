import argparse
import subprocess
# from http import server
# # import os
import struct
import socket

# Returns index of server with best preference
def getPreference(replica_servers_file):
   with open(replica_servers_file, 'r') as f:
         replica_array.append(f.readline().strip())
   preference_array = []
   
   with open(log_file, 'a') as f:
      for ip in replica_array:
         print(f"Pinging {ip} from '{server_ips}'...\n")
         f.write(f"Pinging {ip} from '{server_ips}'...\n")
         pinged = subprocess.run(["ping", ip, "-c", "3"], capture_output=True, text=True)
         output= pinged.stdout.split()

         lossPercent = float(output[-10].split('%')[0])
         delay = float(output[-6].split('ms')[0])
         preference = (0.75*lossPercent) + (0.25*delay)
         print(f"Replica server at {ip}:\n\tLoss: {lossPercent}\tDelay: {delay}\tPreference: {preference}\n")
         f.write(f"Replica server at {ip}:\n\tLoss: {lossPercent}\tDelay: {delay}\tPreference: {preference}\n")
         preference_array.append(preference)
   
   return preference_array.index(min(preference_array))



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



replica_array = []

# get replica with best preference
best_server = getPreference(server_ips)

# Listen for incoming connection from client
while True:
   clientsocket,address=client_sock.accept()
   #Receive header and data        
   header = clientsocket.recv(struct.calcsize('>III'))
   version, msg_type, msg_len = struct.unpack('>III', header)
   data = clientsocket.recv(msg_len)
   print(clientsocket)
   # create header, message, and packet
   version= 17
   msg_type = 1
   msg = (replica_array[best_server]).encode()
   msg_len = len(msg)
   header = s.pack(version, msg_type, msg_len)
   
   # send server ip address to client
   clientsocket.send(header)
   clientsocket.sendall(msg)

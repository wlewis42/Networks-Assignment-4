import argparse
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
args = parser.parse_args()

ip = args.s
port= int(args.p)
logFile = args.l

'''
Validate ip and port number
'''
socket.inet_aton(ip)

if((int(port)) < 0 or (int(port)) > 65535) :
    print("ERROR: invalid port.\n")
    exit()


'''
Loop until DISCONNECT is chosen command
'''
while True:
   user_input = input("Enter a Command (LIGHTON, LIGHTOFF, DISCONNECT): \n")

   '''
   Create client socket
   '''
   clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   #Open logFile
   client_log = open(logFile, "a")

   # connect
   clientsocket.connect((ip,port)) 
   s = struct.Struct("> III")

   version= 17
   msg_type = 0
   helloMess = "HELLO".encode()
   msg_len = len("HELLO")
   header = s.pack(version, msg_type, msg_len)

   client_log.write("Sending HELLO packet\n")
   clientsocket.send(header)
   clientsocket.sendall(helloMess)

   '''
   Functions to send Commands
   '''
   def sendLightOn():
      version= 17
      msg_type = 1
      msg_len = len("LIGHTON")
      lightOn="LIGHTON".encode()
      header = s.pack(version, msg_type, msg_len) + lightOn
      clientsocket.sendall(header)

   def sendLightOff():
      version= 17
      msg_type = 2
      msg_len = len("LIGHTOFF")
      lightOff = "LIGHTOFF".encode()
      header = s.pack(version, msg_type, msg_len) + lightOff
      clientsocket.send(header)

   def sendDisconnect():
      version= 17
      msg_type = 3
      msg_len = len("DISCONNECT")
      disconnect = "DISCONNECT".encode()
      header = s.pack(version, msg_type, msg_len) + disconnect
      clientsocket.send(header)
      clientsocket.close()
      exit()

   header = clientsocket.recv(struct.calcsize('>III'))
   version, msg_type, msg_len = struct.unpack('>III', header)
   data = clientsocket.recv(msg_len) 

   client_log.write(f"Received connection from (IP, PORT): {ip}, {port}\n")
   print(f"Received connection from (IP, PORT): {ip}, {port}\n")

   if(data.decode() == "HELLO"):
      print("Recieved Messaged Hello\n")
      client_log.write("Recieved Messaged Hello\n")

   if(version==17):
      print("VERSION ACCEPTED\n")
      client_log.write("VERSION ACCEPTED\n")
      print("Sending Command\n")
      client_log.write("Sending Command\n")

      if(data.decode() == "Success"):
         print("Received Message SUCCESS\n")
         client_log.write("Received Message SUCCESS\n")
      
   else:
      print("VERSION MISMATCH\n")
      client_log.write("VERSION MISMATCH\n")

   # send correct command
   if (user_input=="LIGHTON"):
      sendLightOn()
   elif (user_input=="LIGHTOFF"):
      sendLightOff()
   elif (user_input=="DISCONNECT"):
      sendDisconnect()

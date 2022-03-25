import argparse
import socket
import struct

#Setting command line arguments
parser = argparse.ArgumentParser(description='Connecting... ')

parser.add_argument("-s", type=str, required=True)
parser.add_argument("-p", type=str, required=True)
parser.add_argument("-l", type=str, required=True)
args = parser.parse_args()

ip = args.s
port= int(args.p)
logFile = args.l

#Checking for valid port and ip
socket.inet_aton(ip)

if((int(port)) < 0 or (int(port)) > 65535) :
    print("\nError invalid port, try agian with a different port number.")
    exit()



while True:
   user_input = input("\nEnter a Command (LIGHTON, LIGHTOFF, DISCONNECT): ")

   # create socket
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   #Open logFile
   file = open(logFile, "a")

   # connect
   client.connect((ip,port)) 
   s = struct.Struct("> III")

   version= 17
   msg_type = 0
   helloMess = "HELLO".encode()
   msg_len = len("HELLO")
   header = s.pack(version, msg_type, msg_len)

   file.write("\nSending HELLO packet")
   client.send(header)
   client.sendall(helloMess)

   def sendLightOn():
      version= 17
      msg_type = 1
      msg_len = len("LIGHTON")
      lightOn="LIGHTON".encode()
      header = s.pack(version, msg_type, msg_len) + lightOn
      client.sendall(header)

   def sendLightOff():
      version= 17
      msg_type = 2
      msg_len = len("LIGHTOFF")
      lightOff = "LIGHTOFF".encode()
      header = s.pack(version, msg_type, msg_len) + lightOff
      client.send(header)

   def sendDisconnect():
      version= 17
      msg_type = 3
      msg_len = len("DISCONNECT")
      disconnect = "DISCONNECT".encode()
      header = s.pack(version, msg_type, msg_len) + disconnect
      client.send(header)
      client.close()
      exit()

   header = client.recv(struct.calcsize('>III'))
   version, msg_type, msg_len = struct.unpack('>III', header)
   data = client.recv(msg_len) 

   file.write(f"Received connection from (IP, PORT): {ip}, {port}")
   print(f"Received connection from (IP, PORT): {ip}, {port}")

   if(data.decode() == "HELLO"):
      print("Recieved Messaged Hello")
      file.write("Recieved Messaged Hello")

   if(version==17):
      print("VERSION ACCEPTED")
      file.write("VERSION ACCEPTED")
      print("Sending Command")
      file.write("Sending Command")

      if(data.decode() == "Success"):
         print("Received Message SUCCESS")
         file.write("Received Message SUCCESS")
      
   else:
      print("VERSION MISMATCH")
      file.write("VERSION MISMATCH")

   # send correct command
   if (user_input=="LIGHTON"):
      sendLightOn()
   elif (user_input=="LIGHTOFF"):
      sendLightOff()
   elif (user_input=="DISCONNECT"):
      sendDisconnect()

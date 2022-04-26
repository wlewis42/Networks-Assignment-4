import argparse
import urllib.request
import socket
import struct

parser = argparse.ArgumentParser(description='Message.')

parser.add_argument('-p', type=str, required=True)
parser.add_argument('-l', type=str, required=True)
parser.add_argument('-w', type=str, required=True)
args = parser.parse_args()

port= int(args.p)
logFile = args.l
webpage = args.w
webpage = 'https://'+webpage

print(port, logFile, webpage)

def download_file(url):
   try:
      file = urllib.request.urlopen(url)
   except:
      file = (f"An error occurred while attempting to download from {url}.")
   return file

web_content = download_file(webpage)
print(web_content.read())
s = struct.Struct("> III")
with open(logFile, "a") as f:
      version = 17
      msg_type = 0
      print(f"Message type: {msg_type}\n")
      f.write(f"Message type: {msg_type}\n")
      msg = web_content.encode()
      msg_len = len(msg)
      header = s.pack(version, msg_type, msg_len)

      print(f"Sending message type: {msg_type} packet\n")
      f.write(f"Sending message type: {msg_type} packet\n")
      
#create server socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()),port))

#listen for connection
while True: 
   server.listen(5)
   conn, address = server.accept()
   conn.send(header)
   conn.sendall(msg)

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

print(port, logFile, webpage)


def download_file(url):
   try:
      file = urllib.request.urlopen(url)
   except:
      file = (f"An error occurred while attempting to download from {url}.")
   return file

web_content = download_file(webpage)
s = struct.Struct("> III")

#create server socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((socket.gethostname(),port))

#listen for connection
while True: 
   server.listen(5)
   conn, address = server.accept()
   conn.sendall(web_content)

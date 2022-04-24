import argparse
from asyncio import subprocess
from http import server

parser = argparse.ArgumentParser(description='Message.')

parser.add_argument('-s', type=str, required=True)
parser.add_argument('-p', type=str, required=True)
parser.add_argument('-l', type=str, required=True)
args = parser.parse_args()

server_ips = args.s
port= int(args.p)
log_file = args.l

replica_array = []

# Returns index of server with best preference
def getPreference(replica_servers_file):
   with open(server_ips, 'r') as f:
      line = f.readline()
      while line:
         line = f.readline()
         replica_array.append(line)

   preference_array = []
   
   with open(log_file, 'a') as f:
      for ip in replica_array:
         f.write(f"Pinging {ip} from '{server_ips}'...")
         pinged = subprocess.run(["ping",ip, "-c", "3"], capture_output = True, text = True)
         f.write(pinged)
         lossPercent = pinged.stdout.split()[-10].split('%')
         delay = pinged.stdout.split()[-6].split('m')
         preference = (0.75*lossPercent) + (0.25*delay)
         f.write(f"Replica server at {ip}:\n\tLoss: {lossPercent}\tDelay: {delay}\tPreference: {preference}")
         preference_array.append(preference)
  
   return preference_array.index(min(preference_array))

# get replica with best preference
best_server = getPreference(server_ips)
with open(log_file, 'a') as f:
   f.write(f"Connecting to {replica_array[best_server]}...")

conn.listen

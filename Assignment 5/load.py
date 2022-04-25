import argparse
import socket
from asyncio import subprocess
import struct

parser = argparse.ArgumentParser(description=' ') 

parser.add_argument("-s", type=str, required=True)
parser.add_argument("-p", type=str, required=True)
parser.add_argument("-l", type=str, required=True)
args = parser.parse_args()

serverIp = args.s
port= int(args.p)
logFile = args.l

def createOutput():
    result = subprocess.run(["ping", IP1, "-c", "3"], capture_output = True, text = True)
    answer = result.stdout
    answerString = answer.split()
    loss = answerString[-10].split('%')
    loss = loss[0]

    delay = answerString[-6].split('m')
    delay = delay[0]

    print("Loss = ", loss)
    print("Delay = ", delay)

    pref1 = (0.75 * loss) + (0.25 * delay)
    print(f"Preference 1: {pref1}")

    result = subprocess.run(["ping", IP2, "-c", "3"], capture_output = True, text = True)
    answer = result.stdout
    answerString = answer.split()
    loss = answerString[-10].split('%')
    loss = loss[0]

    delay = answerString[-6].split('m')
    delay = delay[0]

    print("Loss = ", loss)
    print("Delay = ", delay)

    pref2 = (0.75 * loss) + (0.25 * delay)
    print(f"Preference 2: {pref2}")

    result = subprocess.run(["ping", IP3, "-c", "3"], capture_output = True, text = True)
    answer = result.stdout
    answerString = answer.split()
    loss = answerString[-10].split('%')
    loss = loss[0]
    delay = answerString[-6].split('m')
    delay = delay[0]

    print("Loss = ", loss)
    print("Delay = ", delay)

    pref3 = (0.75 * loss) + (0.25 * delay)
    print(f"Preference 3: {pref3}")

    if pref1 < pref2:
        if pref1 < pref3:
            return IP1
        else:
            return IP3
    else:
        if pref2 < pref1:
            return IP2


while True: 
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.inet_aton("127.0.0.1")

    try:
        serversocket.bind(("127.0.0.1", port))

    except: 
        print("Error, did not bind. Try again with a different port number")
        
    serversocket.listen(5)
    conn, address = serversocket.accept()

    f = open("replica_servers.txt", "r")
    IP1 = f.readline()
    IP2 = f.readline()
    IP3 = f.readline()

    s = struct.Struct(">sI")
    
    mess = createOutput().encode()
    msg_len = len(createOutput)
    header = s.pack(mess, msg_len)

    conn.send(header)
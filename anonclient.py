import argparse
from ipaddress import ip_address
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
parser.add_argument("-f", type=str, required=True)
args = parser.parse_args()

ip = args.s
port= int(args.p)
logFile = args.l
contentfile = args.f


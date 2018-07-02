
from pwn import *

#!/usr/bin/env python
import sys
import struct
import hashlib

# inspired by C3CTF's POW
context.log_level = 'debug'
def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1

def go():
    HOST = "cee810fa.quals2018.oooverflow.io"
    PORT = 31337
    REMOTE = 1
    if(REMOTE):
        s = remote(HOST,PORT)
    else:
        s = remote('192.168.33.10',PORT)
    challenge = s.recvuntil('n:')[-3-10:-3]
    n = int(s.recv(3)[1:])

    print('Solving challenge: "{}", n: {}'.format(challenge, n))

    solution = solve_pow(challenge, n)
    print('Solution: {} -> {}'.format(solution, pow_hash(challenge, solution)))
    s.recvuntil('Solution:')
    s.sendline(str(solution))
    return s

s = go()
s.interactive()

from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('202.182.112.100',PORT)

s.interactive()


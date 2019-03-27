from pwn import *

HOST = ""
PORT = 0
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)

s.interactive()


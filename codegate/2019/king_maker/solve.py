from pwn import *
import random
HOST = "110.10.147.104"
PORT = 13152 
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
raw_input()
s.recvuntil("2> Look around")
s.sendline('1')
s.recvuntil('test 1')
key1 = '\x6c\x4f\x76\x33'
i = 0
s.sendline(key1+chr(i))
s.recvuntil('\n')
print key1
#s.interactive()

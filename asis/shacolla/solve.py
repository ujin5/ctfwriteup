from pwn import *


s = remote('66.172.27.77', 52317)
r = s.recv(4096)
print util.fiddling.hexdump(r)
s.send(r)
s.interactive()


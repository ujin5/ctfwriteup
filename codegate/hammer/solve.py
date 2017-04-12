from pwn import *

s = remote('200.200.200.106', 23254)
s.interactive()

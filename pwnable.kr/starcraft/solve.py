from pwn import *

s = remote('192.168.0.85',1234)
s.interactive()

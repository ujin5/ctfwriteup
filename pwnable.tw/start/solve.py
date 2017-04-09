from pwn import *

s = remote('192.168.50.4',1234)
s.recvuntil('CTF:')

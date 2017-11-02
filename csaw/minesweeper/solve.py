from pwn import *

s = remote('192.168.32.175',31337)

s.interactive()

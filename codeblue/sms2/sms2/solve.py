from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def add(size, content, to, ft):
  s.recvuntil('Select:')
  s.sendline('1')
  s.recvuntil('Size:')
  s.sendline(str(size))
  s.recvuntil('Content:')
  s.send(content)
  s.recvuntil('To:')
  s.send(to)
  s.recvuntil('Select:')
  s.sendline(str(ft))
add(0x10,"ABCD\n",'AAAA\n',1)
s.interactive()


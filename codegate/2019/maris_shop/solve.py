from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('54.180.100.218',PORT)

cart = []

def add_cart(n):
  s.recvuntil(":")
  s.sendline("1")

  r = s.recvuntil("Which item?:")
  r = r.split('\n')
  r = [x.split(".") for x in r]
  del(r[0])
  del(r[len(r)-1])
  idx = 0
  for i in r:
    if i[1] in cart:
      break
  s.sendline(i[0])
  s.recvuntil("?:")
  s.sendline(str(n))
  return r
s.recvuntil(":")
s.sendline("1")
cart.append(r[0][1])
print cart
s.interactive()


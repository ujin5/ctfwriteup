from pwn import *
#s = remote()
asm('mov eax, 5; mov ebx, 0x41414141; xor ecx, ecx; int 0x80;')

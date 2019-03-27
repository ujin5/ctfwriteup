from pwn import *
l = listen(port=7777, bindaddr = "0.0.0.0")

s = l.wait_for_connection()
s.interactive()

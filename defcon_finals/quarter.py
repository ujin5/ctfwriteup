from pwn import *
from wrap import *

def rv():
	r= conv829(bytearray(s.recv()))
	print ''.join(p8(t) for t in r)
def s9(dat):		
	dat = conv928(bytearray(dat+'\n'))
	s.send(bytearray(dat))
s = remote('localhost',1234)
raw_input()
rv()
dat = "1 "*100
s9(dat)
rv()
raw_input()
s9("1454036454")
rv()
for i in xrange(1):
	s9('ps')
	r= conv829(bytearray(s.recv(1024)))
	flag = ''.join(p8(t) for t in r)
flag = flag.split(" ")[:-1]
print flag

rflag = []
for i in flag:
	if i != '0':
		rflag.append(i)

print rflag

res = [int2mid(int(t,10)) for t in rflag]
print res

f = ""
for i in range(len(res)-1, -1, -1):
	f += chr(res[i][0])
	f += chr(res[i][1])
	f += chr(res[i][2])

print f
#s.interactive()

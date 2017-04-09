import base64
s = 'admin'
for i in xrange(20):
  s = base64.encodestring(s)
s = s.replace('1','!')
s = s.replace('2','@')
s = s.replace('3','$')
s = s.replace('4','^')
s = s.replace('5','&')
s = s.replace('6','*')
s = s.replace('7','(')
s = s.replace('8',')')
print s.replace('\n','')

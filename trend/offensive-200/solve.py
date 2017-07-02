from math import sqrt; from itertools import count, islice

def isPrime(n):
    return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))
def check(num):
  if not isPrime(int(num[:2],10)) : return 0
  if not isPrime(int(num[2:4],10)) : return 0
  n = int(num[4:6],10)
  save = n
  i = 0;
  while( n != 0 ):
    if( n < 0 ): return 0;
    n = n - i
    i = i + 2
  if (( save*save^int(num[:4],10) )>>8 == 0) :
    box=list(num)
    j = 0
    for i in range(0,len(box)): j += chr(box[i])
    j = j - 288
    if isPrime(j): return 1;
print(check("236749"))

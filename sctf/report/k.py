from ctypes import *
def todouble(s):
    	cp = pointer(c_int(s))           # make this into a c integer
    	fp = cast(cp, POINTER(c_double))  # cast the int pointer to a float pointer
    	return fp.contents.value         # dereference the pointer, get the float


print todouble(0x41414141)

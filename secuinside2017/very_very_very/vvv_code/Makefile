CXX=g++
#CXXFLAGS=-g3 -O1 -Wall -w -fno-stack-protector -static -m32
CXXFLAGS=-O1 -Wall -w -pedantic -Wl,-z,relro,-z,now -fmessage-length=0 -pie -fPIE
#CXXFLAGS=-std=c++0x -g3 -Wall -w -pedantic -fmessage-length=0 -fno-stack-protector
#CCFLAGS=-g3 -Wall -w -pedantic -fmessage-length=0 -fno-stack-protector 
#CCFLAGS=-g3 -Wall -w -pedantic -fmessage-length=0 -fno-stack-protector -fPIC

O_FILES=	main.o State.o Type.o Utils.o
vvv : $(O_FILES)
	$(CXX) $(CXXFLAGS) -o vvv  $(O_FILES)

# dependency stuff, see: http://www.cs.berkeley.edu/~smcpeak/autodepend/autodepend.html
# pull in dependency info for *existing* .o files
-include $(O_FILES:.o=.d)

.SUFFIXES : .o .cpp

.cpp.o :  
	$(CXX) $(CXXFLAGS) -c $<
	$(CXX) -MM $(CXXFLAGS) $*.cpp > $*.d

clean:
	rm -f vvv *.o *.d

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include "Utils.h"
#include <iostream>
UINT64 read_delim( int fd, char *buf, char delim, int maxlen )
{
	int index = 0;
	char c;

	if ( buf == NULL ) {
		return 0;
	}

	while ( index < maxlen ) {
		if ( read( fd, &c, 1) <= 0 ) {
			std::cout<<"[ERROR] failed to read bytes\n"<<std::endl;
			exit(0);
		}

		if ( c == delim ) {
			return index;
		}

		buf[index] = c;

		index++;
	}

	return index;
}
UINT64 ReadLine(UINT64 n, char *src){
    return read_delim(0,src,'\n',n);
}

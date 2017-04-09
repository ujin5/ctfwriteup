#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define __int64 unsigned long
#define _BYTE char
int main(int argc, char** argv){
  int t = atoi(argv[1]);
    srand(t);
      unsigned int v1 = rand();
        unsigned int v2 = ((((unsigned int)((unsigned __int64)v1 >> 32) >> 30) + (_BYTE)v1) & 3)- ((unsigned int)((unsigned __int64)v1 >> 32) >> 30);
          printf("%lx",v2);
          }

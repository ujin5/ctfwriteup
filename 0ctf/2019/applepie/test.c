#include <stdio.h>         // printf()
#include <string.h>        // strlen()
#include <fcntl.h>         // O_WRONLY
#include <unistd.h>        // write(), close()

int main()
{
   char  *temp = "forum.falinux.comn";
   int    fd;

   if ( 0 < ( fd = open( "/Users/oujin/Downloads/applepie/applepie/flag", O_RDONLY	)))
   {
      write( fd, temp, strlen( temp));
      close( fd);
   }
   else
   {
      printf( "파일 열기에 실패했습니다.n");
   }
   return 0;
}

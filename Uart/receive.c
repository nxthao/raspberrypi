// Compile : gcc -Wall uart-receive.c -o uart-receive -lwiringPi
 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <wiringPi.h>
#include <wiringSerial.h>
 
int main() {
 
	int fd;
	char c;
	printf("Raspberry's receiving : \n");
 
	while(1) {
		if((fd = serialOpen ("/dev/ttyS0", 115200)) < 0 ){
			fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
		}else{
			do{
				c = serialGetchar(fd);
                                if (c == 0x10){

                                        printf("tot \n");
//			        	printf("%X",c);
//			        	fflush (stdout);
                                }
                                else
                                {
                                printf("khong tot \n");
//                                fflush (stdout);
                                }
			}while(serialDataAvail(fd));
		}
             
	}
        printf("het \n");
	return 0;
}

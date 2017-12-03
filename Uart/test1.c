#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>

int main(int argc, char** argv) {
 system("sudo systemctl stop 
        serial-getty@ttyS0.service");
 int sfd = open("/dev/serial0", O_RDWR | O_NOCTTY); 
 if (sfd == -1) {
  printf("Error no is : %d\n", errno);
  printf("Error description is : %s\n", strerror(errno));
  return (-1);
 };
 struct termios options;
 tcgetattr(sfd, &options);
 cfsetspeed(&options, B9600);
 cfmakeraw(&options);
 options.c_cflag &= ~CSTOPB;
 options.c_cflag |= CLOCAL;
 options.c_cflag |= CREAD;
 options.c_cc[VTIME]=0;
 options.c_cc[VMIN]=0;
 tcsetattr(sfd, TCSANOW, &options);
 
 char buf[] = "hello world";
 char buf2[100];
 char c;
 int count = write(sfd, buf,strlen(buf)+1);
 
 int i=0;
 while(1){
  count = read(sfd, &c, 1);
  if(count!=0){
    buf2[i]=c;
    i++;
    if(c==0)break;
  };
 };
 printf("%s\n\r", buf2);close(sfd);
 return (EXIT_SUCCESS);
}

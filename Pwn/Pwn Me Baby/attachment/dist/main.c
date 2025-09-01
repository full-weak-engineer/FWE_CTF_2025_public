#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
void flag(){
  char buf[128]={0};
  int fd=open("flag.txt",O_RDONLY);
  if(fd==-1){
    puts("Couldn't find flag.txt");
    return;
  }
  read(fd,buf,128);
  puts(buf);
}
int main(void){
  char buf[16];
  printf("I will receive a message and do nothing else:");
  scanf("%s",buf);
  return 0;
}

__attribute__((constructor)) void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}
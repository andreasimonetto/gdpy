#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>

unsigned char buf[4096];

int main(int argc, char* const* argv)
{
int fd = open("/dev/gdpymod", O_RDWR);
unsigned long* addr;
int i;

  if(fd < 0) {
    printf("[-] Open failed!\n");
    return -1;
  }

  for(i = 0; i < 4096; ++i)
    buf[i] = (i % 64);

  write(fd, buf, 4096);
  close(fd);
  return 0;
}

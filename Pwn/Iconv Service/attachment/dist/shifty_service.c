// gcc -O0 -Wl,-z,relro,-z,now -fno-pie -no-pie -fstack-protector -z noexecstack -o shifty_service shifty_service.c

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <iconv.h>
#include <errno.h>
#include <stdlib.h>

#define BUFF_SIZE 0x100

typedef struct {
    char buf[BUFF_SIZE];
    size_t left;
} Buffer;

__attribute__((constructor)) void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main(void) {
    Buffer bufs[3];
    int i;
    for(i = 0; i < 3; i++) {
        bufs[i].left = 0;
        memset(bufs[i].buf, 0, sizeof(bufs[i].buf));
    }
    while (1) {
        printf("1: input | 2: output | 3: convert | 4: exit\n> ");

        int cmd;
        if (scanf("%d", &cmd) != 1) {
            break;
        }

        int index;
        if (cmd == 1) {
            printf("Index to input (0-2) > ");
            scanf("%d", &index);
            if (index < 0 || index >= 3) {
                printf("Invalid buffer index\n");
                return 1;
            }
            printf("Input to bufs[%d] > ", index);
            ssize_t len = read(0, bufs[index].buf, BUFF_SIZE);
            if (len <= 0) {
                perror("read");
                return 1;
            } else {
                bufs[index].left = len;
            }
        } else if (cmd == 2) {
            int index;
            printf("Index to output (0-2) > ");
            scanf("%d", &index);
            if (index < 0 || index >= 3) {
                printf("Invalid buffer index\n");
                return 1;
            }
            printf("Output from bufs[%d] >\n", index);
            printf("%s\n", bufs[index].buf);
        } else if (cmd == 3) {
            int src, dst;
            char from[32], to[32];
            printf("Source index (0-2) > ");
            scanf("%d", &src);
            printf("Destination index (0-2) > ");
            scanf("%d", &dst);
            printf("From encoding > ");
            scanf("%31s", from);
            printf("To encoding > ");
            scanf("%31s", to);

            iconv_t cd = iconv_open(to, from);
            if (cd == (iconv_t)-1) {
                perror("iconv_open");
                return 1;
            }
        
            char *inptr = bufs[src].buf;
            size_t inleft = bufs[src].left;
        
            char *outptr = bufs[dst].buf;
            bufs[dst].left = BUFF_SIZE;
        
            size_t res = iconv(cd, &inptr, &(bufs[src].left), &outptr, &(bufs[dst].left));
            if (res == (size_t)-1) {
                perror("iconv");
            } else {
                bufs[dst].left = BUFF_SIZE - bufs[dst].left;
            }
            iconv_close(cd);
        } else {
            printf("Bye\n");
            break;
        }
    }

    return 0;
}

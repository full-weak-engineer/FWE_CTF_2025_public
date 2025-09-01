#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

char *chunks[8];

void menu() {
    puts("1. malloc");
    puts("2. free");
    puts("3. edit");
    puts("4. show");
    puts("5. exit");
    printf("> ");
}

void allocate() {
    int idx;
    size_t size;
    printf("Index: ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= 8) {
        puts("Invalid index");
        return;
    }
    printf("Size: ");
    scanf("%lu", &size);
    chunks[idx] = malloc(size);
    if (!chunks[idx]) {
        puts("Allocation failed");
        exit(1);
    }
    printf("Data: ");
    read(0, chunks[idx], size);
}

void delete() {
    int idx;
    printf("Index: ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= 8) {
        puts("Invalid index");
        return;
    }
    free(chunks[idx]);
}

void edit() {
    int idx;
    printf("Index: ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= 8) {
        puts("Invalid index");
        return;
    }
    if (!chunks[idx]) {
        puts("Invalid chunk");
        return;
    }
    printf("Data: ");
    read(0, chunks[idx], 0x100);
}

void show() {
    int idx;
    printf("Index: ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= 8) {
        puts("Invalid index");
        return;
    }
    if (!chunks[idx]) {
        puts("Invalid chunk");
        return;
    }
    write(1, chunks[idx], 0x100);
}

int main() {
    init();
    puts("Welcome to guided heap!");
    while (1) {
        menu();
        int choice;
        scanf("%d", &choice);
        switch (choice) {
            case 1: allocate(); break;
            case 2: delete(); break;
            case 3: edit(); break;
            case 4: show(); break;
            case 5: exit(0);
            default: puts("Invalid choice");
        }
    }
}

// This problem assumes a libc leak and system("/bin/sh").
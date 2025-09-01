#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef unsigned int u32;
typedef unsigned char u8;

size_t readline(unsigned char *buf, size_t size) {
    if (size == 0) return 0;

    size_t i;
    for (i = 0; i < size - 1; i++) {
        ssize_t n = read(0, &buf[i], 1);
        if (n == -1) exit(1);
        if (n == 0 || buf[i] == '\n') break;
    }
    buf[i] = '\0';
    return i;
}

int get_num(char *prom) {
    printf("%s", prom);
    char buf[0x10] = {};
    readline(buf, sizeof(buf));
    return atoi(buf);
}

void menu() {
    puts("1. set filter");
    puts("2. reset filter");
    puts("3. send data");
    puts("4. exit");
}

enum registers {
    REG_0,
    REG_1,
    REG_2,
    REG_3,
    REG32_0, REG32_1,
    REG32_2, REG32_3,
    REG32_4, REG32_5,
    REG32_6, REG32_7,
};

#define REG_SIZE 8
#define REG_MAX 4
#define REG32_SIZE 4
#define REG32_NUM 8

struct regs {
    union {
        u32 data[REG32_NUM];
        u32 result;
    };
};

enum operations {
    IMM,
    CMP,
    LDR,
};

enum cmp_operations {
    CMP_EQ,
    CMP_LT,
    CMP_GT,
};

struct __attribute__((packed)) imm_args {
    u8 dreg;
    u32 value;
};

struct __attribute__((packed)) cmp_args {
    u8 cmp_op;
    u8 dreg;
    u8 sreg;
    u8 len;
};

struct __attribute__((packed)) ldr_args {
    u8 dreg;
    u8 len;
    u32 offset;
};

struct filter {
    struct filter *next;
    u8 op;
    u8 args[];
};

struct filter *filter_head;
struct filter *filter_tail;

struct data {
    size_t len;
    char str[];
};

size_t reg2idx(enum registers reg) {
    switch(reg) {
    case REG_0...REG_3:
        return reg * REG_SIZE / REG32_SIZE;
    default:
        return reg - REG32_0;
    }
}

int check_reg(enum registers reg) {
    if (reg > REG32_7)
        return -1;
    return 0;
}

int check_widereg(enum registers reg, unsigned int len) {
    if (len == 0)
        return -1;
    switch(reg) {
    case REG_0...REG_3:
        if (reg * REG_SIZE + len > REG32_SIZE * REG32_NUM)
            return -1;
        return 0;
    default:
        if (reg * REG32_SIZE + len > REG32_SIZE * REG32_NUM)
            return -1;
        return 0;
    }
}

void reset_filter() {
    puts("RESETTING FILTER");
    struct filter *cur = filter_head;
    struct filter *next;
    while (cur != NULL) {
        next = cur->next;
        free(cur);
        cur = next;
    }
    filter_head = filter_tail = NULL;
}

void set_filter() {
    struct filter *new;
    enum operations op;
    enum cmp_operations cmp_op;
    enum registers dreg;
    enum registers sreg;
    unsigned int len;
    u32 value;
    u32 offset;

    op = get_num("op: ");
    switch(op) {
    case IMM:
        new = malloc(sizeof(struct filter)+sizeof(struct imm_args));
        if (new == NULL) exit(1);
        dreg = get_num("dreg: ");
        value = get_num("value: ");
        if (check_reg(dreg)) goto err1;
        struct imm_args *imm_args = (struct imm_args*)new->args;
        imm_args->dreg = dreg;
        imm_args->value = value;
        break;
    case CMP:
        new = malloc(sizeof(struct filter)+sizeof(struct cmp_args));
        if (new == NULL) exit(1);
        cmp_op = get_num("cmp_op: ");
        dreg = get_num("dreg: ");
        sreg = get_num("sreg: ");
        len = get_num("len: ");
        if (check_widereg(dreg, len)) goto err1;
        if (check_widereg(sreg, len)) goto err1;
        struct cmp_args *cmp_args = (struct cmp_args*)new->args;
        cmp_args->cmp_op = cmp_op;
        cmp_args->dreg = dreg;
        cmp_args->sreg = sreg;
        cmp_args->len = len;
        break;
    case LDR:
        new = malloc(sizeof(struct filter)+sizeof(struct ldr_args));
        if (new == NULL) exit(1);
        dreg = get_num("dreg: ");
        len = get_num("len: ");
        offset = get_num("offset: ");
        if (check_widereg(dreg, len)) goto err1;
        struct ldr_args *ldr_args = (struct ldr_args*)new->args;
        ldr_args->dreg = dreg;
        ldr_args->len = len;
        ldr_args->offset = offset;
        break;
    default:
        goto err2;
    }
    new->op = op;
    if (filter_head == NULL) {
        filter_head = filter_tail = new;
    } else {
        filter_tail = filter_tail->next = new;
    }
    filter_tail->next = NULL;
    return;

err1:
    puts("INVALID FILTER!");
    free(new);
err2:
    reset_filter();
}

u32 do_filter(struct data *data) {
    struct regs *regs = malloc(sizeof(struct regs));
    memset(regs, 0, sizeof(struct regs));
    for (struct filter *cur = filter_head; cur != NULL; cur = cur->next) {
        switch (cur->op) {
        case IMM:
            struct imm_args *imm_args = (struct imm_args*)cur->args;
            memcpy(&regs->data[reg2idx(imm_args->dreg)], &imm_args->value, 4);
            break;
        case CMP:
            struct cmp_args *cmp_args = (struct cmp_args*)cur->args;
            int ret = memcmp(&regs->data[reg2idx(cmp_args->sreg)], &regs->data[reg2idx(cmp_args->dreg)], cmp_args->len);
            switch(cmp_args->cmp_op) {
            case CMP_EQ:
                (ret == 0) ? (regs->result = 1) : (regs->result = 0);
                break;
            case CMP_LT:
                (ret < 0) ? (regs->result = 1) : (regs->result = 0);
                break;
            case CMP_GT:
                (ret > 0) ? (regs->result = 1) : (regs->result = 0);
                break;
            default:
                exit(1);
            }
            break;
        case LDR:
            struct ldr_args *ldr_args = (struct ldr_args*)cur->args;
            if (ldr_args->offset + ldr_args->len > data->len) {
                puts("(T-T)");
                exit(1);
            }
            memcpy(&regs->data[reg2idx(ldr_args->dreg)], &data->str[ldr_args->offset], ldr_args->len);
            break;
        default:
            exit(1);
        }
    }
    u32 result = regs->result;
    free(regs);
    return result;
}

void send_data() {
    if (filter_head == NULL) {
        puts("SET YOUR FILTER");
        return;
    }
    printf("data: ");
    char buf[0x1000] = {};
    size_t len = readline(buf, sizeof(buf));
    struct data *data = malloc(len+8);
    if (data == NULL) exit(1);
    memcpy(data->str, buf, len);
    data->len = len;
    u32 result = do_filter(data);
    if (result == 1) {
        puts("DETECTED!");
    } else {
        puts(buf);
    }
    free(data);
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    while (1) {
        menu();
        switch (get_num("> ")) {
        case 1:
            set_filter();
            break;
        case 2:
            reset_filter();
            break;
        case 3:
            send_data();
            break;
        case 4:
            return 0;
        default:
            puts("INVALID OPTION");
            break;
        }
    }
}

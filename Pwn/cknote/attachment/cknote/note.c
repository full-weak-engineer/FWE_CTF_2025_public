#include <linux/fs.h>
#include <linux/miscdevice.h>

MODULE_LICENSE("GPL");

#define NOTE_DEVICE_NAME "note"

#define IOCTL_CREATE_NOTE 0x1337000
#define IOCTL_DELETE_NOTE 0x1337001
#define IOCTL_READ_NOTE   0x1337002

#define NOTE_SIZE    0x20
#define MAX_NOTE_NUM 0x200

#define MAX_CREATE_NUM MAX_NOTE_NUM
#define MAX_DELETE_NUM 0x5
#define MAX_READ_NUM 0x2

typedef struct {
    int index;
    void *buf;
} req_t;

struct kmem_cache *note_cache;
struct mutex lock;
char *notes[MAX_NOTE_NUM];
unsigned int counter[3];

static long note_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    req_t req;
    long ret = 0;

    mutex_lock(&lock);

    if (copy_from_user(&req, (void*)arg, sizeof(req)))
        return -EFAULT;
    if (req.index < 0 || req.index >= MAX_NOTE_NUM)
        return -EINVAL;

    switch (cmd) {
    case IOCTL_CREATE_NOTE:
        if (counter[0]++ >= MAX_CREATE_NUM) {
            ret = -EFAULT;
            break;
        }
        if (!notes[req.index]) {
            notes[req.index] = kmem_cache_alloc(note_cache, GFP_KERNEL);
            if (!notes[req.index]) {
                ret = -ENOMEM;
                break;
            }
        }
        if (copy_from_user(notes[req.index], req.buf, NOTE_SIZE)) {
            ret = -EFAULT;
            break;
        }
        break;
    case IOCTL_DELETE_NOTE:
        if (counter[1]++ >= MAX_DELETE_NUM) {
            ret = -EFAULT;
            break;
        }
        kmem_cache_free(note_cache, notes[req.index]);
        break;
    case IOCTL_READ_NOTE:
        if (counter[2]++ >= MAX_DELETE_NUM) {
            ret = -EFAULT;
            break;
        }
        if (copy_to_user(req.buf, notes[req.index], NOTE_SIZE)) {
            ret = -EFAULT;
            break;
        }
        break;
    default:
        ret = -EINVAL;
    }

    mutex_unlock(&lock);
    return ret;
}

static struct file_operations note_fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = note_ioctl,
};

static struct miscdevice note_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = NOTE_DEVICE_NAME,
    .fops = &note_fops,
};

static int __init note_init(void) {
    mutex_init(&lock);
    note_cache = kmem_cache_create("note_cache", NOTE_SIZE, 0, 0, NULL);
    if (!note_cache)
        return -ENOMEM;
    int ret = misc_register(&note_device);
    if (ret) {
        kmem_cache_destroy(note_cache);
        return ret;
    }
    return 0;
}

static void __exit note_exit(void) {
    mutex_lock(&lock);
    for (int i = 0; i < MAX_NOTE_NUM; i++) {
        if (notes[i])
            kmem_cache_free(note_cache, notes[i]);
    }
    mutex_lock(&lock);
    kmem_cache_destroy(note_cache);
    misc_deregister(&note_device);
}

module_init(note_init);
module_exit(note_exit);

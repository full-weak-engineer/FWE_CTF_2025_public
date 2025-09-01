#!/bin/sh

#
# YOUR EXPLOIT HAS BEEN UPLOADED!
#

timeout --foreground 300 qemu-system-x86_64 \
    -m 256M \
    -nographic \
    -kernel bzImage \
    -initrd rootfs.cpio \
    -snapshot \
    -drive file=flag.txt,format=raw \
    -drive file=exploit,format=raw \
    -append "console=ttyS0 pti=on kaslr oops=panic quiet panic=1" \
    -no-reboot \
    -cpu qemu64,+smap,+smep \
    -monitor /dev/null

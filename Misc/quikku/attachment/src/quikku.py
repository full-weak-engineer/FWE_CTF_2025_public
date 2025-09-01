#!/usr/local/bin/python3 -S

import os
import time
import re

def compare(a, b):
    time.sleep(0.0001)
    if a < b:
        return -1
    elif a == b:
        return 0
    return 1


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = []
    middle = []
    right = []
    for x in arr:
        val = compare(x, pivot)
        if val == -1:
            left.append(x)
        elif val == 0:
            middle.append(x)
        else:
            right.append(x)
    return quick_sort(left) + middle + quick_sort(right)

ELAG = "ewectf{th1s_i5_4_3lag_n07_fla9_gg}"
FLAG = os.environ.get("FLAG", "fwectf{this_is_fake_flag_testing_}")
GLAG = "gwectf{gl49_is_n0t_flag_y0u_51lly}"

assert re.match(r"fwectf\{[_0-9a-z]+\}", FLAG) and len(ELAG) == len(FLAG) == len(GLAG)

while True:
    elements = [ELAG, FLAG, GLAG]
    for i in range(100):
        x = input(f"element {i}> ")
        if x == "__END__":
            exit()
        elif len(x) != len(FLAG):
            break
        elements.append(x)
    result = quick_sort(elements)
    print(f"The first is: {result[0]}, and the last is {result[-1]}")
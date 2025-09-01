#!/usr/local/bin/python3 -S
import asyncio
import string

code = ""
while code[-2:] != "\n\n":
    code += input(">>> ") + "\n"

allowed = string.ascii_letters + string.digits + " ()\n:,=\"+-%/\\"

assert all(c in allowed for c in code), "You can't bring that to future..."

fut = asyncio.Future()

_getattr = getattr
_exec = exec

def future(key, *args):
    if key == "__getattribute__":
        raise "Nope"
    return _getattr(asyncio.Future, key)(*args)


for key in dir(__builtins__):
    del __builtins__.__dict__[key]

g = {
    "future": future,
    "fut": fut,
    "__builtins__": {}
}

_exec(code, g, {})
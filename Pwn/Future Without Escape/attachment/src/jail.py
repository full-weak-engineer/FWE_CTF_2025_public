#!/usr/local/bin/python3 -S
import asyncio
import string
import sys, os

code = ""
while code[-2:] != "\n\n":
    code += input(">>> ") + "\n"

allowed = string.ascii_letters + string.digits + " ()\n:,=\"+-%/\\_"

assert all(c in allowed for c in code), "You can't bring that to future..."

fut = asyncio.Future()

_getattr = getattr
_exec = exec

def future(key, *args):
    if key == "__getattribute__":
        raise "Nope"
    return _getattr(fut, key)(*args)

didExec = False
def audit(event, args):
    global didExec
    if event == "exec" and not didExec:
        didExec = True
    elif event != "builtins.id" and didExec:
        os._exit(0)
sys.addaudithook(audit)

for key in dir(__builtins__):
    if key in ["id", "__build_class__"]:
        continue
    del __builtins__.__dict__[key]

g = {
    "__builtins__": {
        "__build_class__": __build_class__,
        "id": id,
    },
    "future": future,
    "__name__": "fwejail",
}


_exec(code, g, {})
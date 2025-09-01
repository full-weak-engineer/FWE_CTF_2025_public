#!/usr/local/bin/python3 -S
import string
import base64

allowed = string.ascii_uppercase + string.digits

code = input("enter your base64 code> ")
assert all(x in allowed for x in code)
code = base64.b64decode(code.encode())
exec(code)

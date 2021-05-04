#!/usr/bin/python
import os
os.chdir("C:\\Users\\Angus\\Desktop\\sdrtest")
from subprocess import Popen, PIPE
import sys

os.chdir("C:\\Users\\Angus\\Desktop\\sdrtest")
cmd = "PYdump.bat"
 
p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")

## But do not wait till netstat finish, start displaying output immediately ##
while True:
    output, error = p.communicate()
    print(output)
    print(p)
    if error:
        print('error:', error, file=sys.stderr)
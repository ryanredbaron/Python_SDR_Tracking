#!/usr/bin/python
import subprocess, sys
import os
os.chdir("C:\\Users\\Angus\\Desktop\\sdrtest")
## command to run - tcp only ##
cmd = "PYdump.bat"
 
## run it ##
p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
 
## But do not wait till netstat finish, start displaying output immediately ##
while True:
    out = p.stderr.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()
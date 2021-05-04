
import subprocess
import os
os.chdir("C:\\Users\\Angus\\Desktop\\sdrtest")
p1 = subprocess.Popen("dump1090.exe --interactive --net --net-ro-size 500 --net-ro-rate 5 --net-buffer 5 --net-beast --mlat", shell=True, stdout=subprocess.PIPE)

print(p1.communicate()[0])
# import subprocess
# cmd = '/home/chan/code/AliceOJ/AliceOJWeb/temp/judger /home/chan/code/AliceOJ/AliceOJWeb/temp/exe_1_1'
# proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out, err = proc.communicate()

# print(out.decode())
# print(err.decode())

import os
res = os.system("gcc main.c")
print(res)
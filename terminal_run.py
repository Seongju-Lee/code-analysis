import os, sys
import subprocess
### count_vs_sum.py 분석
# os.system("pedal feedback code_analysis.py ./count_vs_sum.py")
# cmd = [ 'echo', 'arg1', 'arg2' ]
### arithmethic.py 분석
# os.system("pedal feedback code_analysis.py ./student.py")
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,)
# output = proc.communicate()[0]
# print(output.decode('ISO-8859-2').strip())
# # subprocess 모듈을 사용하여 리턴값 저장 가능

import locale
os_encoding = locale.getpreferredencoding()
cmd = [ ... ]
po = subprocess.Popen("pedal feedback code_analysis.py ./student.py", stdout=subprocess.PIPE)
po.wait()
out = po.stdout.read().decode('UTF-8').strip()

print(out)
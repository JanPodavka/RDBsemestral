import subprocess
import time


def exportdata(n):

    process2 = subprocess.Popen([r"E:\VS_TUL_navazujici\2_semestr\DBS\app\RDBsemestral\semestral.exe", str(n)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

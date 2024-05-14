import subprocess
import time

def exportdata(n):
    # Spusťte váš program v C++
    zdrojovy_soubor = r"C:\Users\osoukup\source\repos\ConsoleApplication1\ConsoleApplication1\ConsoleApplication1.cpp"
    process = subprocess.Popen([r"C:\Users\osoukup\mingw64\bin\g++", zdrojovy_soubor, "-o", "program"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.5)
    process2 = subprocess.Popen(["./program",n], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
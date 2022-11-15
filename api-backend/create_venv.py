from pickle import TRUE
import subprocess
import time
import os
venvname = ".backendvenv"
p = subprocess.Popen(f"python -m venv {venvname}", shell=True)
while p.poll() is None:
    continue
print(p.communicate())
p = subprocess.Popen(
    f"{os.getcwd()}\\{venvname}\\Scripts\\python.exe -m pip install -r venvdependencies.txt", shell=True)
while p.poll() is None:
    continue
print(p.communicate())
p = subprocess.Popen(
    f"{os.getcwd()}\\{venvname}\\Scripts\\python.exe -m pip freeze", shell=True)
while p.poll() is None:
    continue
print(p.communicate())

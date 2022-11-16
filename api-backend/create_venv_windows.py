from pickle import TRUE
import subprocess
import time
import os
# This script deploys a venv in the folder it is executed.
# Currently only works for Windows.
# Might require a different python executable name
# depending on the system.
venvname = ".backendvenv"
# Create the venv in the working directory
p = subprocess.Popen(f"python -m venv {venvname}", shell=True)
while p.poll() is None:
    continue
print(p.communicate())
# Install dependencies in the venv using pip.
# Requires a file named venvdependencies.txt
# containing the backend dependecies (in pip freeze format)
# in the working directory.
p = subprocess.Popen(
    f"{os.getcwd()}\\{venvname}\\Scripts\\python.exe -m pip install -r venvdependencies.txt", shell=True)
while p.poll() is None:
    continue
print(p.communicate())

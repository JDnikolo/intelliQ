import subprocess

class TestInit:
    #Test 1
    def test_Init(self):
        subprocess.Popen(["python", "login.py", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"]).wait()
        process = subprocess.Popen(["python", "resetall.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        output, errors = process.communicate()
        print(errors)
        logout = subprocess.Popen(["python", "logout.py"])
        logout.wait()
import subprocess

class TestInit:
    #Test 1
    def test_Init(self):
        subprocess.Popen(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"]).wait()
        process = subprocess.Popen(["python", "resetall"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        output, errors = process.communicate()
        print(errors)
        subprocess.Popen(["python", "logout"])
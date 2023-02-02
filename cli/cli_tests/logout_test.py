import subprocess

class TestLogout:
    #Test 1
    def test_right_output(self):
        subprocess.run(["python", "login.py", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "logout.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"You have successfully logged out." in output
    
    #Test 2 
    def test_relogout(self):
        process = subprocess.Popen(["python", "logout.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"401" in output
        assert b"Invalid or missing access token" in output
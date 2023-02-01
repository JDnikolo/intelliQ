import subprocess

class TestLogin:
    #Test 1
    def test_right_output(self):
        process = subprocess.Popen(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"Welcome back, andreane82! You have successfully logged in." in output
    
    # no relogin error in new login endpoint
    #Test 2 
    # def test_relogin(self):
    #     process = subprocess.Popen(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     output, errors = process.communicate()
    #     print(errors)
    #     assert b"400" in output
    #     assert b"Already logged in." in output

    #Test 3
    def test_bad_username(self):
        process = subprocess.Popen(["python", "login", "--username", "andreane85", "--passw", "e00f8e21a864de304a6c"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"401" in output
        assert b"Invalid Credentials" in output

    #Test 4
    def test_bad_password(self):
        process = subprocess.Popen(["python", "login", "--username", "andreane82", "--passw", "e00f8ee304a6c"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"401" in output
        assert b"Invalid Credentials" in output    
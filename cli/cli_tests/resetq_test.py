import subprocess

class TestResetQ:
    #Test 1
    def test_OK(self):
        subprocess.run(["python", "login.py", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "resetq.py", "--questionnaire_id", "QQ000","--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"status\": \"OK" in output
    
    #Test 2
    def test_no_answers(self):
        process = subprocess.Popen(["python", "resetq.py", "--questionnaire_id", "QQ876","--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"status\":\"failed", "reason\":\"No answers found" in output
        
    #Test 3
    def test_unauthorized(self):
        subprocess.run(["python", "logout"])
        process = subprocess.Popen(["python", "resetq.py", "--questionnaire_id", "QQ876","--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"User is unauthorized" in output
        subprocess.run(["python", "login.py", "--username", "user55", "--passw", "12345"])
        process = subprocess.Popen(["python", "resetq.py", "--questionnaire_id", "QQ876","--format", "json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"User is unauthorized" in output
        
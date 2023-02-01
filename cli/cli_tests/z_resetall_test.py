import subprocess

#file_path contains path to json file to be uploaded
file_path = "../test/dummy_data_files/fill_data.json"

class TestResetAll:
    #Test 1
    def test_OK(self):
        subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        subprocess.Popen(["python", "questionnaire_upd", "--source", file_path],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = subprocess.Popen(["python", "resetall"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"status\": \"OK" in output
        
    #Test 2
    def test_no_available_questionnaires(self):
        subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "resetall"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"User andreane82 has no available questionnaires" in output
    
    #Test 3
    def test_unauthorized(self):
        subprocess.run(["python", "logout"])
        process = subprocess.Popen(["python", "resetall"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"User is unauthorized" in output
        subprocess.run(["python", "login", "--username", "user55", "--passw", "12345"])
        process = subprocess.Popen(["python", "resetall"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"User is unauthorized" in output
        
import subprocess

#file_path contains path to json file to be uploaded
file_path = "../test/dummy_data_files/TrekkingClubQuestionnaire.json"

class TestQuestionnaireUpd:
    #Test 1
    def test_200(self):
        login = subprocess.run(["python", "login.py", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        login.wait()
        process = subprocess.Popen(["python", "questionnaire_upd.py", "--source", file_path],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b'200' in output
    #Test 2
    def test_already_exists(self):
        process = subprocess.run(["python", "login.py", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "questionnaire_upd.py", "--source", file_path],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"400" in output
        assert b'Questionnaire ID already exists.' in output
    #Test 3
    def test_anauthorized(self):
            process = subprocess.run(["python", "logout.py"])
            process = subprocess.Popen(["python", "questionnaire_upd.py", "--source", file_path],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()
            print(errors)
            assert b"401" in output
            assert b"Unauthorized" in output
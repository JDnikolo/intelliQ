import subprocess

class TestQuestionnaire:
    #Test 1
    def test_200(self):
        subprocess.run(["python", "login.py", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "questionnaire.py", "--questionnaire_id", "QQ000", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"200" in output
    
    #Test 2
    def test_bad_questionnaire(self):
        process = subprocess.Popen(["python", "questionnaire.py", "--questionnaire_id", "QK700", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"400" in output
        assert b"The requested questionnaire is not present in the database." in output
   
    #Test 3
    def test_bad_questionnaireid_format(self):
        process = subprocess.Popen(["python", "questionnaire.py", "--questionnaire_id", "Q00", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"400" in output
        assert b"Required field was not given or is incorrectly formatted." in output 
    
    #Test 4
    def test_wrong_format(self):
        process = subprocess.Popen(["python", "questionnaire.py", "--questionnaire_id", "QQ000", "--format","jsonnaire"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"invalid choice: 'jsonnaire' (choose from 'csv', 'json')" in errors
    #Test 5
    def test_csv_format_reply(self):
        process = subprocess.Popen(["python", "questionnaire.py", "--questionnaire_id", "QQ000", "--format","csv"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"csv file QQ000.csv saved at csv_files directory successfully" in output
    #Test 6
    def test_unauthorized(self):
        subprocess.run(["python", "logout.py"])
        process = subprocess.Popen(["python", "questionnaire.py", "--questionnaire_id", "QQ000","--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"401" in output
        assert b"User is unauthorized" in output
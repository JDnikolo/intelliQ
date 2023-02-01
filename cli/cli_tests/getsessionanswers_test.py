import subprocess

class TestGetSessionAnswers:
    #Test 1
    def test_200(self):
        process = subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "getsessionanswers", "--questionnaire_id", "QQ000", "--session_id", "temp", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"200" in output
    
    #Test 2
    def test_test_no_answers(self):
        process = subprocess.Popen(["python", "getsessionanswers", "--questionnaire_id", "QQ900", "--session_id", "temp123", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"402" in output
        assert b"No answers were found." in output
   
    #Test 3
    def test_wrong_format(self):
        process = subprocess.Popen(["python", "getsessionanswers", "--questionnaire_id", "QQ000", "--session_id", "temp", "--format","jsonnaire"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"invalid choice: 'jsonnaire' (choose from 'csv', 'json')" in errors
    #Test 4
    def test_csv_format_reply(self):
        process = subprocess.Popen(["python", "getsessionanswers", "--questionnaire_id", "QQ000", "--session_id", "temp", "--format","csv"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"csv file temp.csv saved at csv_files directory successfully" in output
    #Test 5
    def test_unauthorized(self):
        process = subprocess.run(["python", "logout"])
        process = subprocess.Popen(["python", "getsessionanswers", "--questionnaire_id", "QQ000", "--session_id", "temp","--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
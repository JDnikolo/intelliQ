import subprocess

class TestDoAnswer:
    #Test 1
    def test_200(self):
        process = subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "doAnswer", "--questionnaire_id", "QQ000", "--question_id", "Q01", "--session_id", "temp", "--option_id", "Q01A3","--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"Answer submitted successfully." in output
    #Test 2
    def test_bad_data(self):
        process = subprocess.Popen(["python", "doanswer", "--questionnaire_id", "QQ900", "--question_id", "Q50", "--session_id", "temp", "--option_id", "Q01A3","--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"400" in output
        assert b"Bad request parameters" in output
    #Test 3
    def test_wrong_format(self):
        process = subprocess.Popen(["python", "doAnswer", "--questionnaire_id", "QQ000", "--question_id", "Q00", "--session_id", "temp", "--option_id", "Q01A3","--format","jsonnaire"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"invalid choice: 'jsonnaire' (choose from 'csv', 'json')" in errors
    #Test 4
    def test_csv_format_reply(self):
        process = subprocess.Popen(["python", "doAnswer", "--questionnaire_id", "QQ000", "--question_id", "Q01", "--session_id", "temp", "--option_id", "Q01A3","--format","csv"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"Answer submitted successfully." in output
    #Test 5
    def test_unauthorized(self):
        process = subprocess.run(["python", "logout"])
        process = subprocess.Popen(["python", "doAnswer", "--questionnaire_id", "QQ000", "--question_id", "Q00", "--session_id", "temp", "--option_id", "Q01A3","--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"401" in output
        assert b"User is unauthorized" in output
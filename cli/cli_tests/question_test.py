import subprocess

class TestQuestion:
    #Test 1
    def test_200(self):
        process = subprocess.run(["python", "login", "--username", "andreane82", "--passw", "e00f8e21a864de304a6c"])
        process = subprocess.Popen(["python", "question", "--questionnaire_id", "QQ000", "--question_id", "Q01", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"200" in output
    #Test 2
    def test_non_existing_question(self):
        process = subprocess.Popen(["python", "question", "--questionnaire_id", "QQ000", "--question_id", "Q9000", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"400" in output
        assert b"The requested questionnaire/question is not present in the database." in output
    #Test 3
    def test_non_existing_questionnaire(self):
        process = subprocess.Popen(["python", "question", "--questionnaire_id", "QQ9000", "--question_id", "Q01", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"400" in output
        assert b"The requested questionnaire/question is not present in the database." in output
    #Test 4
    def test_csv_format(self):
        process = subprocess.Popen(["python", "question", "--questionnaire_id", "QQ000", "--question_id", "Q01", "--format","csv"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        print(errors)
        assert b"csv file saved at csv_files directory successfully!" in output
    #Test 5
    def test_unauthorized(self):
            process = subprocess.run(["python", "logout"])
            process = subprocess.Popen(["python", "question", "--questionnaire_id", "QQ000", "--question_id", "Q01", "--format","json"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()
            print(errors)
            assert b"401" in output
            assert b"User is unauthorized" in output
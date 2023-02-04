import unittest
import contextlib
import sys 
from unittest.mock import patch 
from io import StringIO
sys.path.append("..")
from imports import *

#the csv to mock for the get request response
response_csv = '''questionnaireID,qID,qtext,required,type,options

QQ000,Q01,Ποιον προορισμό προτιμάτε για αυτό το ΣΚ;,1,question,"[{'optID': 'Q01A1', 'opttxt': 'Βουνό', 'nextqID': 'Q02'}, {'optID': 'Q01A2', 'opttxt': 'Θάλασσα', 'nextqID': 'Q04'}, {'optID': 'Q01A3', 'opttxt': 'Πεδιάδα', 'nextqID': 'Q04'}]"

''' 
#the json to mock for the get request response
response_json = {'questionnaireID': 'QQ000',
                             'qID': 'Q01', 'qtext': 'Ποιον προορισμό προτιμάτε για αυτό το ΣΚ;', 'required': '1', 'type': 'question', 
                             'options': [{'optID': 'Q01A1', 'opttxt': 'Βουνό', 'nextqID': 'Q02'}, {'optID': 'Q01A2', 'opttxt': 'Θάλασσα', 'nextqID': 'Q04'}, {'optID': 'Q01A3', 'opttxt': 'Πεδιάδα', 'nextqID': 'Q04'}]}

class Question:
    #function that is used in question.py to call the corresponding API endpoint
    def question(self, arg):
        url = 'http://localhost:9103/intelliq_api/question/' + arg.questionnaire_id + '/' + arg.question_id + '?format=' + arg.format
        res = requests.get(url, headers=find_key() , verify=False)
        if (arg.format == 'json' and res.status_code == 200):
                print(res.status_code)
                print(res.json())
        elif (arg.format == 'csv' and res.status_code == 200):
            #write location of csv file changed for tests so we can test its contents
            f = open(f"./question_QQ000_Q01.csv", 'w+', encoding="utf-8") 
            f.truncate(0)
            f.write(res.text())
            f.seek(0)
            f.close()
            print(res.text)
            print("csv file saved at csv_files directory successfully!")
        else:
            print(res.status_code)
            print(res.json())
        return True

#Class used to mock get request responses
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data

    class MockResponseCsv:
        def __init__(self, text_data, status_code):
            self.text_data = text_data
            self.status_code = status_code
        def text(self):
            return self.text_data
    #format = json
    if args[0] == 'http://localhost:9103/intelliq_api/question/QQ000/Q01?format=json':
        return MockResponse(response_json, 200)
    #format = csv
    elif args[0] == 'http://localhost:9103/intelliq_api/question/QQ000/Q01?format=csv':
        return MockResponseCsv(response_csv,200
    )
    return MockResponse(None, 404)

class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(questionnaire_id = "QQ000", question_id = "Q01", format = "json")

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_question_success(self,mock_get):
        #Test json format call
        temp = Question()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.question(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("200",output)
        self.assertIn("'questionnaireID': 'QQ000'",output)
        self.assertIn("'Q01', 'qtext': 'Ποιον προορισμό προτιμάτε για αυτό το ΣΚ;', 'required': '1', 'type': 'question'",output)
        self.assertIn("'options': [{'optID': 'Q01A1', 'opttxt': 'Βουνό', 'nextqID': 'Q02'}, {'optID': 'Q01A2', 'opttxt': 'Θάλασσα', 'nextqID': 'Q04'}, {'optID': 'Q01A3', 'opttxt': 'Πεδιάδα', 'nextqID': 'Q04'}]",output)
        
        #Testing csv format call
        
        self.args = argparse.Namespace(questionnaire_id = "QQ000", question_id = "Q01", format = "csv") 
        temp_stdout2 = StringIO()
        with contextlib.redirect_stdout(temp_stdout2):
            temp.question(self.args)
        with open('question_QQ000_Q01.csv', 'r',encoding="utf-8") as t1, open('./model_csv_files/question_QQ000_Q01.csv', 'r', encoding="utf-8") as t2:
            fileone = t1.readlines()
            filetwo = t2.readlines()
        #Check that the csv that is returned is identical to the model one 
        isSame = True
        with open('temp.csv', 'w') as outFile:
            for line in fileone:
                if line not in filetwo:
                    isSame = False
                    outFile.write(line)                    
        os.remove("temp.csv")           #remove temp csv files used for comparison with the model csv file
        os.remove("question_QQ000_Q01.csv")
        self.assertTrue(isSame)


if __name__ == '__main__':
    unittest.main()
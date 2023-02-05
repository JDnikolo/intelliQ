import unittest
from unittest.mock import patch 
import sys 
import contextlib
from io import StringIO
sys.path.append("..")
from imports import *

#the csv to mock for the get request response
response_csv = '''questionnaireID,session,qID,ans

QQ000,1234

,,P01,P01A1

''' 
#the json to mock for the get request response
response_json = {'questionnaireID': 'QQ000', 'session': '1234', 'answers': [{'qID': 'P01', 'ans': 'P01A1'}]}

class Getsessionanswers:
    #function that is used in getsessionanswers.py to call the corresponding API endpoint
    def getsessionanswers(self, arg):
        url = 'http://localhost:9103/intelliq_api/getsessionanswers/' + arg.questionnaire_id + '/' + arg.session_id
        if (arg.format == 'csv'):
            url = url + '?format=csv'
        res = requests.get(url, headers=find_key(), verify=False)
        if (arg.format == 'json' and res.status_code == 200):
                print(res.status_code)
                print(res.json())
        elif (arg.format == 'csv' and res.status_code == 200):
            f = open(f"./1234.csv", 'w+', encoding="utf-8") 
            f.truncate(0)
            f.write(res.text)
            f.seek(0)
            f.close()
            #print(res.status_code)
            print(res.text)
            print(f"csv file {arg.session_id}.csv saved at csv_files directory successfully")
        else:
            print(res.text)
        return True

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json.dumps(json_data)

        def json(self):
            return self.json_data
    class MockResponseCsv:
        def __init__(self, text_data, status_code):
            self.text = text_data
            self.status_code = status_code
        def text(self):
            return self.text
    if args[0] == 'http://localhost:9103/intelliq_api/getsessionanswers/QQ000/1234':
        return MockResponse(response_json, 200)
    if args[0] == 'http://localhost:9103/intelliq_api/getsessionanswers/QQ000/1234?format=csv':
        return MockResponseCsv(response_csv, 200)    
    return MockResponse(None, 404)

class TestGetsessionanswers(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(questionnaire_id = "QQ000", session_id = "1234", format='json')

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_getsessionanswers_success(self,mock_get):
        #Testing json format call
        temp = Getsessionanswers()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.getsessionanswers(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("200", output)
        self.assertIn("'questionnaireID': 'QQ000', 'session': '1234', 'answers':", output)

        #Testing csv format call
        
        self.args = argparse.Namespace(questionnaire_id = "QQ000", session_id = "1234", format = "csv") 
        temp_stdout2 = StringIO()
        with contextlib.redirect_stdout(temp_stdout2):
            temp.getsessionanswers(self.args)
        with open('1234.csv', 'r', encoding="utf-8") as f1, open('./model_csv_files/1234.csv', 'r', encoding="utf-8") as f2:
            fileone = f1.readlines()
            filetwo = f2.readlines()
        #Check that the csv that is returned is identical to the model one 
        isSame = True
        with open('temp.csv', 'w') as outFile:
            for line in fileone:
                if line not in filetwo:
                    isSame = False
                    outFile.write(line)                    
        os.remove("temp.csv")           #remove temp csv files used for comparison with the model csv file
        os.remove("1234.csv")
        self.assertTrue(isSame)


if __name__ == '__main__':
    unittest.main()
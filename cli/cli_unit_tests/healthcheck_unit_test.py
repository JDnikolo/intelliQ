import unittest
from unittest.mock import patch 
import sys 
import contextlib
from io import StringIO
sys.path.append("..")
from imports import *

#the csv to mock for the get request response
response_csv = '''status,dbconnection

OK,intelliq

''' 
#the json to mock for the get request response
response_json = {'status': 'OK', 'dbconnection': 'intelliq'}

class Healthcheck:
    #function that is used in healthcheck.py to call the corresponding API endpoint
    def healthcheck(self,arg):
        url = 'http://localhost:9103/intelliq_api/admin/healthcheck'
        if (arg.format == 'csv'):
            url = url + '?format=csv'
        res = requests.get(url, headers=find_key(), verify=False)
        if (arg.format == 'json' and res.status_code == 200):
            print(res.status_code)
            print(res.json())
        elif (arg.format == 'csv' and res.status_code == 200):
            #write location of csv file changed for tests so we can test its contents
            f = open("./healthcheck.csv", 'w+') 
            f.truncate(0)
            f.write(res.text())
            f.seek(0)
            f.close()
            print(res.status_code)
            print(res.text)
            print("csv file healthcheck.csv saved at csv_files directory successfully")
        else:
            print(res.json())
        return True

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
    if args[0] == 'http://localhost:9103/intelliq_api/admin/healthcheck':
        return MockResponse(response_json, 200)
    if args[0] == 'http://localhost:9103/intelliq_api/admin/healthcheck?format=csv':
        return MockResponseCsv(response_csv, 200)    
    return MockResponse(None, 404)

class TestHealthcheck(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(format='json')

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_healthcheck_success(self,mock_get):
        #Testing json format call
        temp = Healthcheck()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.healthcheck(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("200", output)
        self.assertIn("'status': 'OK'", output)
        self.assertIn("'dbconnection': 'intelliq'",output)

        #Testing csv format call
        
        self.args = argparse.Namespace(format = "csv") 
        temp_stdout2 = StringIO()
        with contextlib.redirect_stdout(temp_stdout2):
            temp.healthcheck(self.args)
        with open('healthcheck.csv', 'r',encoding="utf-8") as f1, open('./model_csv_files/healthcheck.csv', 'r', encoding="utf-8") as f2:
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
        os.remove("healthcheck.csv")
        self.assertTrue(isSame)


if __name__ == '__main__':
    unittest.main()
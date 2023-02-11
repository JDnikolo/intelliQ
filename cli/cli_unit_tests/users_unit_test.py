import unittest
from unittest.mock import patch
import sys
import contextlib
from io import StringIO
sys.path.append("..")
from imports import *

#the csv to mock for the get request response
response_csv = '''username,password,user_type,access_token

user123456,123456,V,token_value


''' 

#the json to mock for the get request response
response_json = "{'username': 'user123456', 'password': '123456', 'user_type': 'V', 'access_token': 'token_value'}"

#json used to mock error mesage
response_error = {"type": "/errors/operation-error",
                        "title": "Missing required fields.",
                        "status": "400",
                        "detail": "Expecting error details here!",
                        "instance": "/admin/users"}

class Users:
    #function that is used in admin.py to call the corresponding API endpoint(users)
    def users(self,arg):
        url = 'http://localhost:9103/intelliq_api/admin/users/' + arg.username + '?format=' + arg.format
        res = requests.get(url, headers=find_key(), verify=False)
        if(res.status_code == 200):
            print("User data :")
            if (arg.format == 'json'):
                print(res.json())
            else:
                #write location of csv file changed for tests so we can test its contents
                f = open(f"./userinfo_{arg.username}.csv", 'w+') 
                f.truncate(0)
                f.write(res.text())
                f.seek(0)
                f.close()
                print(res.text())
                print(f"{arg.username} info saved at csv_files directory successfully!")  
        else:
            error = res.json()
            print(error['detail'])
        return True

#Mocks the get request according to the url specified
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
    if args[0] == 'http://localhost:9103/intelliq_api/admin/users/user123456?format=json':
        return MockResponse(response_json, 200)
    if args[0] == 'http://localhost:9103/intelliq_api/admin/users/user123456?format=csv':
        return MockResponseCsv(response_csv, 200)    
    if args[0] == 'http://localhost:9103/intelliq_api/admin/users/WrongUser?format=json':
        return MockResponse(response_error, 400) 
    return MockResponse(None, 404)

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(username='user123456',format='json')

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_users_success(self,mock_get):
        #Testing json format call
        temp = Users()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.users(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn('''User data :\n{'username': 'user123456', 'password': '123456', 'user_type': 'V', 'access_token': 'token_value'}''', output)

        #Testing csv format call
        self.args = argparse.Namespace(username='user123456',format = "csv") 
        temp_stdout2 = StringIO()
        with contextlib.redirect_stdout(temp_stdout2):
            temp.users(self.args)
        with open('userinfo_user123456.csv', 'r',encoding="utf-8") as f1, open('./model_csv_files/userinfo_model.csv', 'r', encoding="utf-8") as f2:
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
        os.remove("userinfo_user123456.csv")
        self.assertTrue(isSame)

        #Testing error message
        self.args = argparse.Namespace(username = 'WrongUser', format = 'json') 
        temp_stdout3 = StringIO()
        with contextlib.redirect_stdout(temp_stdout3):
            temp.users(self.args)
        output3 = temp_stdout3.getvalue().strip()
        self.assertIn("Expecting error details here!", output3)

if __name__ == '__main__':
    unittest.main()
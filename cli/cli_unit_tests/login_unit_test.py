import unittest
import contextlib
import sys 
from unittest.mock import patch 
from io import StringIO
sys.path.append("..")
from imports import *

#the json to mock for the post request response
json_response ={"token": 12345}
 
class Login:
    #function that is used in doAnswer.py to call the corresponding API endpoint
    def login(self, arg):
    
        info = {'username': arg.username, 'password': arg.passw}
        res = requests.post('http://localhost:9103/intelliq_api/login', data=info, verify=False)

        jsonres = res.json()

        if (res.status_code == 200):
            print(jsonres['token'])
            home = str(Path.home())
            f = open(home + '/softeng22API.token', 'w')
            f.write(jsonres['token'])
            f.close()
            print(f"Welcome back, andreane82! You have successfully logged in.")
            sys.exit(0)
        else:
            print(res.text)
        return True


#Class used to mock post request responses
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json.dumps(json_data)
        def json(self):
            return self.json_data

    if args[0] == 'http://localhost:9103/intelliq_api/login':
        return MockResponse(json_response, 200)
    return MockResponse(None, 404)

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace()

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_login_success(self,mock_post):
        #Test call
        temp = Login()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.login(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("Welcome back, andreane82! You have successfully logged in.", output)


if __name__ == '__main__':
    unittest.main()
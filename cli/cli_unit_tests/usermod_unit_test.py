import unittest
from unittest.mock import patch
import sys 
import contextlib
from io import StringIO
sys.path.append("..")
from imports import *

#json used to mock unauthorized call
json_response = '''{"type": "/errors/authorization-error",
                        "title": "Unauthorized.",
                        "status": "401",
                        "detail": "You are not authorized to use this endpoint.",
                        "instance": "/admin/usermod"}'''
                        
#json used to mock error mesage
json_response_error = {"type": "/errors/operation-error",
                        "title": "Incorrect credential length.",
                        "status": "400",
                        "detail": "Expecting error details here!",
                        "instance": "/admin/usermod"}

class Usermod:
    #function that is used in admin.py to call the corresponding API endpoint(usermod)
    def usermod(self,arg):
        url = 'http://localhost:9103/intelliq_api/admin/usermod/' + arg.username + '/' + arg.passw
        res = requests.post(url, headers=find_key(), verify=False)
        if(res.status_code == 401):
            print("You are unauthorized to perform this action!")
        if(res.status_code == 200):
            print("User Registered/password updated Successfully!\n")
        if(res.status_code == 400):
            error = res.json()
            print(error["detail"])
        return True

#Mocks the post request according to the url specified
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    if args[0] == 'http://localhost:9103/intelliq_api/admin/usermod/user123456/123456':
        return MockResponse({}, 200) 
    if args[0] == 'http://localhost:9103/intelliq_api/admin/usermod/NotAdmin/somepassw':
        return MockResponse(json_response, 401)
    if args[0] == 'http://localhost:9103/intelliq_api/admin/usermod/BadUser/BadPassw':
        return MockResponse(json_response_error, 400)
    return MockResponse(None, 404)

class TestUsermod(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(username = 'user123456', passw = '123456')

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_usermod_success(self,mock_post):

        #Testing authorized call
        temp = Usermod()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.usermod(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("User Registered/password updated Successfully!", output)

        #Testing unauthorized call
        self.args = argparse.Namespace(username = 'NotAdmin', passw = 'somepassw') 
        temp_stdout2 = StringIO()
        with contextlib.redirect_stdout(temp_stdout2):
            temp.usermod(self.args)
        output2 = temp_stdout2.getvalue().strip()
        self.assertIn("You are unauthorized to perform this action!", output2)

        #Testing error message
        self.args = argparse.Namespace(username = 'BadUser', passw = 'BadPassw') 
        temp_stdout3 = StringIO()
        with contextlib.redirect_stdout(temp_stdout3):
            temp.usermod(self.args)
        output3 = temp_stdout3.getvalue().strip()
        self.assertIn("Expecting error details here!", output3)


if __name__ == '__main__':
    unittest.main()
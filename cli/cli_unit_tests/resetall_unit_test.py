import unittest
import contextlib
import sys 
from unittest.mock import patch 
from io import StringIO
sys.path.append("..")
from imports import *

#the json to mock for the post request response
json_response ={
  "status": "OK"
}

class ResetAll:
    #function that is used in questionnaire_upd.py to call the corresponding API endpoint
    def resetall(self):
        res = requests.post('http://localhost:9103/intelliq_api/admin/resetall',
                      headers=find_key(),
                      verify=False)
        if(res.status_code == 200):
            print(res.json())
        else:
            error = res.json()
            print(error['detail'])
        return True

#Class used to mock post request responses
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
    if args[0] == 'http://localhost:9103/intelliq_api/admin/resetall':
        return MockResponse(json_response, 200)
    return MockResponse(None, 404)

class TestResetAll(unittest.TestCase):

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_resetall_success(self,mock_post):
        #Test call
        temp = ResetAll()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.resetall()
        output = temp_stdout.getvalue().strip()
        self.assertIn("status\': \'OK", output)

if __name__ == '__main__':
    unittest.main()
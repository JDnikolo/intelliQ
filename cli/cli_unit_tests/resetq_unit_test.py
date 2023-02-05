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

class Resetq:
    #function that is used in questionnaire_upd.py to call the corresponding API endpoint
    def resetq(self, arg):
        url = 'http://localhost:9103/intelliq_api/admin/resetq/' + arg.questionnaire_id
        res = requests.post(url, headers=find_key(), verify=False)
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
    if args[0] == 'http://localhost:9103/intelliq_api/admin/resetq/QQ000':
        return MockResponse(json_response, 200)
    return MockResponse(None, 404)

class TestResetq(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(questionnaire_id = "QQ000", format = "json")

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_resetq_success(self,mock_post):
        #Test call
        temp = Resetq()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.resetq(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("status\": \"OK", output)

if __name__ == '__main__':
    unittest.main()
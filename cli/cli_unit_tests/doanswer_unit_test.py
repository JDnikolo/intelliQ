import unittest
import contextlib
import sys 
from unittest.mock import patch 
from io import StringIO
sys.path.append("..")
from imports import *

#the json to mock for the post request response
json_response ={"status": "Successful"}
 
class DoAnswer:
    #function that is used in doAnswer.py to call the corresponding API endpoint
    def doanswer(self, arg):
        url = 'http://localhost:9103/intelliq_api/doanswer/' + arg.questionnaire_id + '/' + arg.question_id + '/' + arg.session_id + '/' + arg.option_id
        res = requests.post(url, headers=find_key(), verify=False)
        if(res.status_code==200):
            print("Answer submitted successfully.")
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

    if args[0] == 'http://localhost:9103/intelliq_api/doanswer/QQ000/P01/1234/P01A1':
        return MockResponse(json_response, 200)
    return MockResponse(None, 404)

class TestDoAnswer(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(questionnaire_id = "QQ000", question_id = "P01", session_id = "1234", option_id = "P01A1", format = "json")

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_doAnswer_success(self,mock_post):
        #Test call
        temp = DoAnswer()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.doanswer(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("Answer submitted successfully.", output)


if __name__ == '__main__':
    unittest.main()
import unittest
import contextlib
import sys 
from unittest.mock import patch 
from io import StringIO
sys.path.append("..")
from imports import *

#the json to mock for the post request response
json_response ={
                "type":"/success",
                "title": "OK",
                "status": "200",
                "detail":"Questionnaire inserted successfully.",
                "instance":"/admin/questionnaire_upd"}

#Path to json file to be uploaded
json_source ="../../test/dummy_data_files/TrekkingClubQuestionnaire.json"

class Questionnaire_upd:
    #function that is used in questionnaire_upd.py to call the corresponding API endpoint
    def questionnaire_upd(self,arg):
        url = 'http://localhost:9103/intelliq_api/admin/questionnaire_upd'

        res = requests.post(url,
                            headers=find_key(),
                            files={'file': open(arg.source,'rb')},
                            verify=False)
        print(res.status_code)
        print(res.json())
        return True

#Class used to mock post request responses
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
    #check if the uploaded file is the desired one. If not, return 404 status code
    for key,value in kwargs.items():
        if (key == 'files'):
            for key2,value2 in value.items():
                if(key2 == 'file' and value2.name != json_source):
                    return MockResponse("Failed to Upload",404)
    if args[0] == 'http://localhost:9103/intelliq_api/admin/questionnaire_upd':
        return MockResponse(json_response, 200)
    return MockResponse(None, 404)

class TestQuestionnaireUpd(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(source = json_source)

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_questionnaire_upd_success(self,mock_post):
        #Test call
        temp = Questionnaire_upd()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.questionnaire_upd(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("200",output)
        self.assertIn("'type': '/success'", output)
        self.assertIn("'title': 'OK'", output)
        self.assertIn("'detail': 'Questionnaire inserted successfully.'", output)
        self.assertIn("'instance': '/admin/questionnaire_upd'", output)


if __name__ == '__main__':
    unittest.main()
import unittest
import contextlib
import sys 
from unittest.mock import patch 
from io import StringIO
sys.path.append("..")
from imports import *

#the json to mock for the post request response
json_response ={}
 
class Logout:
    #function that is used in doAnswer.py to call the corresponding API endpoint
    def logout(self):
        res = requests.post('http://localhost:9103/intelliq_api/logout',
                            headers=find_key(),
                            verify=False)
        #print(res.status_code)
        if (res.status_code == 200):
            home = str(Path.home())
            if os.path.exists(home + '/softeng22API.token'):
                os.remove(home + '/softeng22API.token')
            print("You have successfully logged out.")
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

    if args[0] == 'http://localhost:9103/intelliq_api/logout':
        return MockResponse(json_response, 200)
    return MockResponse(None, 404)

class TestLogout(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace()

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_logout_success(self,mock_post):
        #Test call
        temp = Logout()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.logout()
        output = temp_stdout.getvalue().strip()
        self.assertIn("You have successfully logged out.", output)


if __name__ == '__main__':
    unittest.main()
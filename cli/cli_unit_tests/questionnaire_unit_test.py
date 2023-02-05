import unittest
from unittest.mock import patch 
import sys 
import contextlib
from io import StringIO
sys.path.append("..")
from imports import *

#the csv to mock for the get request response
response_csv = '''"('QQ000',)","[('Ερωτηματολόγιο Προορισμού Εκδρομής Trekking Club',)]","[('poll',), ('trekking',), ('vacation',)]","[('P00', 'Ποιο είναι το mail σας;', 0, 'profile'), ('P01', 'Ποια είναι η ηλικία σας;', 1, 'profile'), ('Q01', 'Ποιον προορισμό προτιμάτε για αυτό το ΣΚ;', 1, 'question'), ('Q02', 'Εφόσον απαντήσατε [*Q01A1] στην προηγούμενη ερώτηση, τι θα προτιμούσατε;', 1, 'question'), ('Q03', 'Εφόσον διαλέξατε [*Q02A3], πληκτρολογήστε την προτίμησή σας:', 1, 'question'), ('Q04', 'Τι διάρκεια θα θέλατε να έχει η εκδρομή;', 1, 'question'), ('Q05', 'Τι ποσό θα θέλατε να διαθέσετε;', 1, 'question'), ('Q06', 'Εφόσον απαντήσατε [*Q05A1] στην ερώτηση [*Q05], θα θέλατε να συνεισφέρετε στο κοινό ταμείο της οργάνωσης για την εκδρομή;', 0, 'question'), ('Q07', 'Θα είστε με παρέα ή χωρίς;', 0, 'question')]"

''' 
#the json to mock for the get request response
response_json = {'questionnaireID': ['QQ000'], 'questionnaireTitle': [['Ερωτηματολόγιο Προορισμού Εκδρομής Trekking Club']], 'keywords': [['poll'], ['trekking'], ['vacation']], 'questions': [['P00', 'Ποιο είναι το mail σας;', 0, 'profile'], ['P01', 'Ποια είναι η ηλικία σας;', 1, 'profile'], ['Q01', 'Ποιον προορισμό προτιμάτε για αυτό το ΣΚ;', 1, 'question'], ['Q02', 'Εφόσον απαντήσατε [*Q01A1] στην προηγούμενη ερώτηση, τι θα προτιμούσατε;', 
1, 'question'], ['Q03', 'Εφόσον διαλέξατε [*Q02A3], πληκτρολογήστε την προτίμησή σας:', 1, 'question'], ['Q04', 'Τι διάρκεια θα θέλατε να έχει η εκδρομή;', 1, 'question'], ['Q05', 'Τι ποσό θα θέλατε να διαθέσετε;', 1, 'question'], ['Q06', 'Εφόσον απαντήσατε [*Q05A1] στην ερώτηση [*Q05], θα θέλατε να συνεισφέρετε στο κοινό ταμείο της οργάνωσης για την εκδρομή;', 0, 'question'], ['Q07', 'Θα είστε με παρέα ή χωρίς;', 0, 'question']]}

class Questionnaire:
    #function that is used in questionnaire.py to call the corresponding API endpoint
    def questionnaire(self, arg):
        url = 'http://localhost:9103/intelliq_api/questionnaire/' + arg.questionnaire_id
        if (arg.format == 'csv'):
            url = url + '?format=csv'
        res = requests.get(url, headers=find_key(), verify=False)
        if (arg.format == 'json' and res.status_code == 200):
                print(res.status_code)
                print(res.json())
        elif (arg.format == 'csv' and res.status_code == 200):
            #write location of csv file changed for tests so we can test its contents
            f = open(f"./QQ000.csv", 'w+', encoding="utf-8") 
            f.truncate(0)
            f.write(res.text)
            f.seek(0)
            f.close()
            #print(res.status_code)
            print(res.text)
            print(f"csv file QQ000.csv saved at csv_files directory successfully")
        else:
            print(res.status_code)
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
    if args[0] == 'http://localhost:9103/intelliq_api/questionnaire/QQ000':
        return MockResponse(response_json, 200)
    if args[0] == 'http://localhost:9103/intelliq_api/questionnaire/QQ000/?format=csv':
        return MockResponseCsv(response_csv, 200)    
    return MockResponse(None, 404)

class TestQuestionnaire(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(questionnaire_id = "QQ000", format='json')

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_questionnaire_success(self,mock_get):
        #Testing json format call
        temp = Questionnaire()
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            temp.questionnaire(self.args)
        output = temp_stdout.getvalue().strip()
        self.assertIn("200", output)

        #Testing csv format call
        
        self.args = argparse.Namespace(questionnaire_id = "QQ000", format = "csv") 
        temp_stdout2 = StringIO()
        with contextlib.redirect_stdout(temp_stdout2):
            temp.questionnaire(self.args)
        with open('QQ000.csv', 'r',encoding="utf-8") as f1, open('./model_csv_files/QQ000.csv', 'r', encoding="utf-8") as f2:
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
        os.remove("{arg.questionnaire_id}.csv")
        self.assertTrue(isSame)


if __name__ == '__main__':
    unittest.main()
from imports import *

#TODO test csv functionality when added to endpoint
def getquestionanswers(arg):
  #print(arg)
  url = 'http://localhost:9103/intelliq_api/getquestionanswers/' + arg.questionnaire_id + '/' + arg.question_id
  if (arg.format == 'csv'):
        url = url + '?format=csv'
  res = requests.get(url, headers=find_key(), verify=False)
  if (arg.format == 'json' and res.status_code == 200):
        print(res.status_code)
        print(res.json())
  elif (arg.format == 'csv' and res.status_code == 200):
    f = open(f"./csv_files/{arg.question_id}.csv", 'w+', encoding="utf-8") 
    f.truncate(0)
    f.write(res.text)
    f.seek(0)
    f.close()
    print(res.text)
    print(f"csv file {arg.question_id}.csv saved at csv_files directory successfully")
  else:
    print(res.text)
  return True


parser = argparse.ArgumentParser()
parser.add_argument('--questionnaire_id', help='Enter questionnaire_id', required='TRUE')
parser.add_argument('--question_id', help='Enter question_id whose answers you need', required='TRUE')
parser.add_argument('--format',
                    choices=['csv', 'json'],
                    help='Select json or csv format',
                    required='TRUE')
args = parser.parse_args()

getquestionanswers(args)

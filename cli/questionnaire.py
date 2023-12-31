from imports import *


def questionnaire(arg):
  url = 'http://localhost:9103/intelliq_api/questionnaire/' + arg.questionnaire_id
  if (arg.format == 'csv'):
    url = url + '?format=csv'
  res = requests.get(url, headers=find_key(), verify=False)
  if (arg.format == 'json' and res.status_code == 200):
        print(res.status_code)
        print(res.json())
  elif (arg.format == 'csv' and res.status_code == 200):
    f = open(f"./csv_files/{arg.questionnaire_id}.csv", 'w+', encoding="utf-8") 
    f.truncate(0)
    f.write(res.text)
    f.seek(0)
    f.close()
    #print(res.status_code)
    print(res.text)
    print(f"csv file {arg.questionnaire_id}.csv saved at csv_files directory successfully")
  else:
    print(res.status_code)
    print(res.json())
  return True



parser = argparse.ArgumentParser()
parser.add_argument('--questionnaire_id',
                    help='Enter id of questionnaire whose info you need',
                    required='TRUE')
parser.add_argument('--format',
                    choices=['csv', 'json'],
                    help='Select json or csv format',
                    required='TRUE')
args = parser.parse_args()

questionnaire(args)

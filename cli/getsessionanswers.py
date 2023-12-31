from imports import *


def getsessionanswers(arg):
  url = 'http://localhost:9103/intelliq_api/getsessionanswers/' + arg.questionnaire_id + '/' + arg.session_id
  if (arg.format == 'csv'):
    url = url + '?format=csv'
  res = requests.get(url, headers=find_key(), verify=False)
  if (arg.format == 'json' and res.status_code == 200):
        print(res.status_code)
        print(res.json())
  elif (arg.format == 'csv' and res.status_code == 200):
    f = open(f"./csv_files/{arg.session_id}.csv", 'w+', encoding="utf-8") 
    f.truncate(0)
    f.write(res.text)
    f.seek(0)
    f.close()
    #print(res.status_code)
    print(res.text)
    print(f"csv file {arg.session_id}.csv saved at csv_files directory successfully")
  else:
    print(res.text)
  return True


parser = argparse.ArgumentParser()
parser.add_argument('--questionnaire_id', help='Enter questionnaire_id', required='TRUE')
parser.add_argument('--session_id', help='Enter session_id', required='TRUE')
parser.add_argument('--format',
                    choices=['csv', 'json'],
                    help='Select json or csv format',
                    required='TRUE')
args = parser.parse_args()

getsessionanswers(args)

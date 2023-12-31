from imports import *


def question(arg):
  url = 'http://localhost:9103/intelliq_api/question/' + arg.questionnaire_id + '/' + arg.question_id + '?format=' + arg.format
  res = requests.get(url, headers=find_key() , verify=False)
  if (arg.format == 'json' and res.status_code == 200):
        print(res.status_code)
        print(res.json())
  elif (arg.format == 'csv' and res.status_code == 200):
    
    f = open(f"./csv_files/question_{arg.questionnaire_id}_{arg.question_id}.csv", 'w+', encoding="utf-8") 
    f.truncate(0)
    f.write(res.text)
    f.seek(0)
    f.close()
    print(res.text)
    print("csv file saved at csv_files directory successfully!")
  else:
    print(res.status_code)
    print(res.json())
  return True


parser = argparse.ArgumentParser()
parser.add_argument('--questionnaire_id', help='Questionnaire ID that the desired question belongs to.', required='TRUE')
parser.add_argument('--question_id', help='ID of the desired question.', required='TRUE')
parser.add_argument('--format',
                    choices=['csv', 'json'],
                    help='Select json or csv format.',
                    required='TRUE')
args = parser.parse_args()

question(args)

from imports import *


def doanswer(arg):
  #print(arg)
  url = 'http://localhost:9103/intelliq_api/doanswer/' + arg.questionnaire_id + '/' + arg.question_id + '/' + arg.session_id + '/' + arg.option_id
  #take api key from file saved from login
  headers = None
  home = str(Path.home())
  if os.path.exists(home + '/softeng22API.token'):
    f = open(home + '/softeng22API.token', 'r')
    content = f.read()
    headers = {'x-observatory-auth': content}
  res = requests.post(url, headers=headers, verify=False)
  if(res.status_code==200):
        print("Answer submitted successfully.")
  else:
    print(res.text)
  return True


parser = argparse.ArgumentParser()
parser.add_argument('--questionnaire_id', help='Enter id of questionnaire', required='TRUE')
parser.add_argument('--question_id', help='Enter id of question', required='TRUE')
parser.add_argument('--session_id', help='Enter session_id', required='TRUE')
parser.add_argument('--option_id', help='Enter option_id', required='TRUE')
# not needed
parser.add_argument('--format',
                    choices=['csv', 'json'],
                    help='Select json or csv format',
                    required='TRUE')
args = parser.parse_args()

doanswer(args)

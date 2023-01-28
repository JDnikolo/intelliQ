from imports import *


def resetq(arg):
  url = 'http://localhost:9103/intelliq_api/admin/resetq/' + arg.questionnaire_id
  res = requests.post(url, headers=find_key(), verify=False)
  print(res.text)
  return True


parser = argparse.ArgumentParser()
parser.add_argument(
  '--questionnaire_id',
  help='Enter id of questionnaire whose answers you want to delete',
  required='TRUE')
#not needed
parser.add_argument('--format',
                    choices=['csv', 'json'],
                    help='Select json or csv format',
                    required='TRUE')
args = parser.parse_args()

resetq(args)

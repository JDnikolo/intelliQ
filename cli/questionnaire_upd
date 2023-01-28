from imports import *


def questionnaire_upd(arg):
  url = 'http://localhost:9103/intelliq_api/admin/questionnaire_upd'

  res = requests.post(url,
                      headers=find_key(),
                      files={'file': open(arg.source,'rb')},
                      verify=False)
  print(res.status_code)
  print(res.json())
  return True


parser = argparse.ArgumentParser()
parser.add_argument('--source',
                    help='Select a questionnaire .json file to upload',
                    required='TRUE')
#TODO fix source if needed with .csv
args = parser.parse_args()
questionnaire_upd(args)
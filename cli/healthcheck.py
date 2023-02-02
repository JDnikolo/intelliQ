from imports import *

def healthcheck(arg):
  url = 'http://localhost:9103/intelliq_api/admin/healthcheck'
  if (arg.format == 'csv'):
    url = url + '?format=csv'
  res = requests.get(url, headers=find_key(), verify=False)
  if (arg.format == 'json' and res.status_code == 200):
    print(res.status_code)
    print(res.json())
  elif (arg.format == 'csv' and res.status_code == 200):
    f = open("./csv_files/healthcheck.csv", 'w+') 
    f.truncate(0)
    f.write(res.text)
    f.seek(0)
    f.close()
    #print(res.status_code)
    print(res.text)
    print("csv file healthcheck.csv saved at csv_files directory successfully")
  else:
    print(res.json())
  return True


parser = argparse.ArgumentParser()
parser.add_argument('--format',
                    choices=['csv', 'json'],
                    help='Select json or csv format',
                    required='TRUE')
args = parser.parse_args()

healthcheck(args)

from imports import *

def login(arg):

  info = {'username': arg.username, 'password': arg.passw}
  res = requests.post('http://localhost:9103/intelliq_api/login', data=info, verify=False)

  jsonres = res.json()

  if (res.status_code == 200):
    print(jsonres['token'])
    home = str(Path.home())
    f = open(home + '/softeng22API.token', 'w')
    f.write(jsonres['token'])
    f.close()
    print(f"Welcome back, {arg.username}! You have successfully logged in.")
    sys.exit(0)
  else:
    print(res.text)
  return True


parser = argparse.ArgumentParser()
parser.add_argument('--username', help='Enter username', required='TRUE')
parser.add_argument('--passw', help='Enter password', required='TRUE')
args = parser.parse_args()

login(args)
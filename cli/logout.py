from imports import *

def logout():
  res = requests.post('http://localhost:9103/intelliq_api/logout',
                      headers=find_key(),
                      verify=False)
  #print(res.status_code)
  if (res.status_code == 200):
    home = str(Path.home())
    if os.path.exists(home + '/softeng22API.token'):
      os.remove(home + '/softeng22API.token')
    print("You have successfully logged out.")
  else:
        print(res.text)
  return True

logout()
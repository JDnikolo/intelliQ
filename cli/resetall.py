from imports import *


def resetall():
  res = requests.post('http://localhost:9103/intelliq_api/admin/resetall',
                      headers=find_key(),
                      verify=False)
  if(res.status_code == 200):
    print(res.json())
  else:
    error = res.json()
    print(error['detail'])
  return True


resetall()

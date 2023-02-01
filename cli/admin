from imports import *


def usermod(arg):
  url = 'http://localhost:9103/intelliq_api/admin/usermod/' + arg.username + '/' + arg.passw
  res = requests.post(url, headers=find_key(), verify=False)
  if(res.status_code == 401):
    print("You are unauthorized to perform this action!")
  if(res.status_code == 200):
    print("User Registered/password updated Successfully!\n")
  else:
    error = res.json()
    print(error['detail'])
  return True


def users(arg):
  url = 'http://localhost:9103/intelliq_api/admin/users/' + arg.username + '?format=' + arg.format
  res = requests.get(url, headers=find_key(), verify=False)
  if(res.status_code == 200):
    print("User data :")
    if (arg.format == 'json'):
      print(res.json())
    else:
      f = open(f"./csv_files/userinfo_{arg.username}.csv", 'w+') 
      f.truncate(0)
      f.write(res.text)
      f.seek(0)
      f.close()
      print(res.text)
      print(f"{arg.username} info saved at csv_files directory successfully!")  
  else:
    error = res.json()
    print(error['detail'])
  return True

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prefix_chars='/')

  sub = parser.add_subparsers()
  #usermod
  usermod_parser = sub.add_parser('--usermod')
  usermod_parser.add_argument('--username', help = 'The username of the new user or that of an existing user', required = 'TRUE')
  usermod_parser.add_argument('--passw', help = 'The new users password or the existing user\'s updated password', required = 'TRUE')
  usermod_parser.set_defaults(func = usermod)
  
  #users
  users_parser = sub.add_parser('--users')
  users_parser.add_argument('--username', help = 'The username of the user whose information will be shown.', required = 'TRUE')
  users_parser.add_argument('--format',
                    choices=['csv', 'json'],
                    help='Select json or csv format.',
                    required='TRUE')
  users_parser.set_defaults(func = users)
  
  args = parser.parse_args()

  if hasattr(args, 'func'):
    if args.func.__name__ == 'usermod':
      usermod(args)
    elif args.func.__name__ == 'users':
      users(args)
  else:
    parser.print_help()
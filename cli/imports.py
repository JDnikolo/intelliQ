import argparse
import requests
import json
from prettytable import from_csv
from prettytable import DEFAULT
from pathlib import Path
import os

def find_key():
    #take api key from file saved from login
    headers = None
    home = str(Path.home())
    if os.path.exists(home + '/softeng22API.token'):
        f = open(home + '/softeng22API.token', 'r')
        content = f.read()
        headers = {'x-observatory-auth': content}
        return headers
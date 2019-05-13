import requests
import argparse
import json
import random

KEY = "25821352e1d420315f04ab8239a625e7"
API = "https://wall.alphacoders.com/api2.0/get.php"

PARAMS = {'auth':KEY, "method":"category",'id':'1'}

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
r = json.loads(requests.get(API, params=PARAMS).text)
if r['success']:
    print(r['wallpapers'])
    for  i in r['wallpapers']:
        key = random.randint(1, 100)
        if key  == 100:
            print('ok, key is ', key )
            break
        else:
            print('pass, key was ', str(key))
else:
    print('wops!')

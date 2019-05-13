#!/bin/python3
import requests
import argparse
import json
import random
import os
KEY = "25821352e1d420315f04ab8239a625e7"
API = "https://wall.alphacoders.com/api2.0/get.php"

PARAMS = {'auth':KEY, "method":"category",'id':'1',
'page':str(random.randint(1,5)), 'width': '2160',
'height':'1080', 'operator':'min'}

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
def set_wall(file_name):
    mon_list = os.popen('xfconf-query -c \
    xfce4-desktop -l | grep "workspace0/last-image"').read().split()
    for i in mon_list:
        print(i)
        os.system('xfconf-query \
        --channel xfce4-desktop --property '+ i +' --set ' + file_name)

r = json.loads(requests.get(API, params=PARAMS).text)
if r['success']:
    #print(r['wallpapers'])
    for i in r['wallpapers']:
        key = random.randint(1, 100)
        if key >= 95:
            print('ok, key is ', key,'\nPrinting out wall')
            print('downloading', i['url_image'], '...', end = ' ')
            download(i['url_image'], '/tmp/temp.jpg')
            print('ok!')#узнать бы как это более централизованно сделать
            set_wall('/tmp/temp.jpg')
            break
        else:
            print('pass, key was ', str(key))
else:
    print('wops!')

#!/bin/python3
import requests, json, random, os, sys, sqlworker, config

CPARAMS = {'auth':config.KEY, "method":"category_list"}

sql = sqlworker.Sql('temp/tt.db')

if not os.path.exists(config.MAIN_FOLDER):
    print("This installation is incorrect! can`t see " + MAIN_FOLDER\
     + " folder!", file=sys.stderr)
    exit(1)

def get_categories():
    list = []
    r = json.loads(requests.get(config.API, params=CPARAMS).text)
    for i in r['categories']:
        if i['name'] != 'Abstract':
            list.append('!' + i['name'] + '::category_')
        else:
            list.append(i['name'] + '::category_')
    return list

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

def set_wall(file_name):
    mon_list = os.popen('/usr/bin/xfconf-query -c \
    xfce4-desktop -l | grep "workspace0/last-image"').read().split()
    for i in mon_list:
        print(i)
        os.system('xfconf-query \
        --channel xfce4-desktop --property '+ i +' --set ' + file_name)

class Walld(object):
    DEBUG = 1
    '''this class represents all walld functions except trays one'''

    def __init__(self):
        print('class walld started!')

    def current_image(self, store = False):
        #сохранить бы в файл если честно
        if store:
            self.var = store
        else:
            return self.var

    def save_image(self, name = False):
        if not name:
            self.save_path =  MAIN_FOLDER+'/saved/' + str(random.random())
        else:
            self.save_path = name
        os.system('cp ' + MAIN_FOLDER+'/temp.jpg ' + self.save_path)# имя бы достать
        print('saved at ' + self.save_path)

    def guess_de(self):
        pass#need to guess current de

    def add_option(self, name):
        sql.change_option()
        pass
    def spin_dice(self, chance):
        list = []
        for i in range(0, 10000):
            PARAMS = {'auth':KEY, "method":"category",'id':'1',
            'page':i, 'width': '1920',
            'height':'1080', 'operator':'min'}
            r = json.loads(requests.get(API, params=PARAMS).text)
            print('getting ', i)
            if r['success']:
                if r['wallpapers']:
                    list += r['wallpapers']
                else:
                    print('breaking!')
                    break
            else:
                print('whoops')
            #print(r['wallpapers'])
        for i in list:
            key = random.randint(0, 100)# IDEA: ЧО ЕСЛИ ВЗЯТЬ ВЕСЬ СПИСОК И ТОЛЬКО ПО НЕМУ УЖЕ ХУЯЯЧИТЬ ТОЕСТЬ РАСПАРСИТЬ ВСЕ СТРАНИЧКИ И ЕБАШИТЬ УЖЕ ПО НЕМУ ПРОЦЕНТАМИ
            if key >= chance:
                print('ok, key is ' + str(key) +'\nPrinting out wall')
                print('downloading', i['url_image'], '...', end = ' ')
                download(i['url_image'], MAIN_FOLDER+'/temp.jpg')
                print('ok!')#узнать бы как это более централизованно сделать
                set_wall(MAIN_FOLDER+'/temp.jpg')
                break
            else:
                print('pass, key was '+ str(key))
        else:
            print('wops!')

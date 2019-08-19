'this is the core of walld, all functions should store here'
import sqlite3
import json
import random
import pickle
import sys
import os
import requests
import config

def get_categories():
    '''gets a list of all categories by api method'''
    list_categories = []
    params = {'auth':config.KEY, "method":"category_list"}
    json_answer = json.loads(requests.get(config.API, params=params).text)
    for i in json_answer['categories']:
        if i['name'] != 'Abstract':
            list_categories.append('!' + i['name'] + '::cat_')
        else:
            list_categories.append(i['name'] + '::cat_')
    return list_categories

def download(url, file_name):
    '''downloads a file, first comes url, second comes full path of file'''
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    return file_name


class Walld():
    '''this class represents almost all walld functions except trays one'''
    def __init__(self):
        self.save_path = config.MAIN_FOLDER+'/saved/' + str(random.random())
        self.desktop_environment = os.popen("env | grep DESKTOP_SESSION= \
        | awk -F= '{print $2}'").read()

        if not os.path.exists(config.MAIN_FOLDER):
            print("This installation is incorrect! can`t see "\
            + config.MAIN_FOLDER + " folder!", file=sys.stderr)
            exit(1)
        print('class walld started!')

    def save_image(self, name=False):
        '''copy image to specific(if passed) folder or to standart
        self.save_path path'''
        if name:
            os.system('cp ' + config.MAIN_FOLDER+'/temp.jpg ' + name)
            print('saved at ' + name)
        else:
            os.system('cp ' + config.MAIN_FOLDER+'/temp.jpg ' + self.save_path)
            print('saved at ' + self.save_path)

    def spin_dice(self):
        '''making a list of urls by accessing a db, than sets wall'''
        list_of_urls = []
        for i in FILER.get_cells('Abstract'):
            list_of_urls.append(i[4])
        self.set_wall(download(random.choice(list_of_urls),\
         config.MAIN_FOLDER+'/temp.jpg'))

    def set_wall(self, file_name):
        '''this is critical module, depending on de it sets walls'''
        print('this is de' + self.desktop_environment)
        if self.desktop_environment == 'xfce\n':
            mon_list = os.popen('/usr/bin/xfconf-query -c \
            xfce4-desktop -l | grep "workspace0/last-image"').read().split()
            for i in mon_list:
                os.system('/usr/bin/xfconf-query \
                --channel xfce4-desktop --property '+ i +' --set ' + file_name)
        elif self.desktop_environment == 'mate\n': #experimental
            os.system('/usr/bin/gsettings set org.mate.background\
            picture-filename'+ file_name)
        elif self.desktop_environment == 'gnome\n': #experimental
            os.system('/usr/bin/gsettings set \
            org.gnome.desktop.background picture-uri file://'+ file_name)

    def change_option(self, name, add=False):
        '''need to rewrite it'''
        print(FILER.settings)
        if add:
            print('adding', name)
            FILER.settings.append(name)
        else:
            print('removing', name)
            FILER.settings.remove(name)
            FILER.dump()

class Filer:
    '''Abstraction for files and settings'''
    def __init__(self, db_name):
        self.db_name = db_name
        if not os.path.exists(config.MAIN_FOLDER):
            print('creating!' + config.MAIN_FOLDER)
            os.mkdir(config.MAIN_FOLDER)
        print('filer class is started, checking db!')
        try:
            self.conn = sqlite3.connect(config.DB_NAME)
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM pics")
            print('found db!')
        except sqlite3.OperationalError:
            print('need to download db!')
            download(config.DB_URL, config.DB_NAME)
            print('ok!')
            print('connecting!')
            self.conn = sqlite3.connect(config.DB_NAME)
            self.cursor = self.conn.cursor()
        print('checking options!')
        try:
            with open(config.SETTINGS_FILE, 'rb') as file:
                self.settings = pickle.load(file)
        except FileNotFoundError:
            print('file not found! creating new one')
            self.settings = []
            self.dump()

#    def add_option(self, name): # не очень это красиво, брат
#        '''this function add tags to settings'''
#        self.change_option(name, add=True)

#    def remove_option(self, name):
#        '''this function remove tags to settings'''
#        self.change_option(name)

    def dump(self):
        '''this function dumps settings to file'''
        with open(config.SETTINGS_FILE, 'wb') as temp:
            pickle.dump(self.settings, temp)

    def get_cells(self, category):
        '''this function get cells by category'''
        sql = "SELECT * FROM pics WHERE category='{}'".format(category)
        self.cursor.execute(sql)
        return self.cursor.fetchall()


FILER = Filer(config.DB_NAME)

def get_settings():
    '''gets list of settings'''
    return FILER.settings

'this is the core of walld, all functions should store here'
import ctypes  # MANY THANKS TO J.J AND MESKSR DUDES YOU SAVED MY BURNED UP ASS
import json
from collections import namedtuple
import os
import platform
import random
import shutil
import subprocess  # nosec
from pathlib import Path
from helpers import SubCat

from requests import get

from helpers import download

#stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python

MAIN_FOLDER = Path().home() / '.walld'
URL_LOG = MAIN_FOLDER / 'walld.log' # get it from settings!

class Walld():
    '''this class represents almost all walld functions except trays one'''
    def __init__(self, api, main_folder=MAIN_FOLDER):
        self.main_folder = main_folder
        self.api = api
        self.prefs = self.main_folder / 'prefs.json'
        # self.save_path = (self.main_folder+'/saved/' +
        #                   str(random.random()) + '.png')#nosec
        # self.main_folder_temp = self.main_folder + '/temp.jpg'

        if platform.system() == 'Windows': #here comes windows specific stuff
            self.desktop_environment = platform.system()

        else:
            code = ("/usr/bin/env | /usr/bin/grep DESKTOP_SESSION= "
                    "| /usr/bin/awk -F= '{print $2}'")
            self.desktop_environment = \
            subprocess.check_output(code, shell=True).decode('ascii')#nosec, redo

        self._sync_categories()
        # print('class walld started!')
        # log.info class walld started

    def save_image(self, name=None):
        '''copy image to specific(if passed)
           folder or to standart
           self.save_path path'''
        if name:
            shutil.copyfile(self.main_folder_temp, name)#nosec
            print('saved at ' + name)

        else:
            shutil.copyfile(self.main_folder_temp,
                            self.save_path) # nosec wont fix
            print('saved at ' + self.save_path)
            self.save_path = (f'{self.main_folder}/saved/'
                              f'{str(random.random())}.png') # nosec

    def spin_dice(self):
        '''making a list of urls by accessing a db, than sets wall'''
        new_url = self.get_urls()['url']
        # log.info(new_url)
        self.set_wall(download(new_url,\
        self.main_folder+'/temp.jpg'))

    def set_wall(self, file_name):
        '''this is critical module, depending on DE it sets walls'''
        if self.desktop_environment == 'xfce\n':
            mon_list = subprocess.check_output('/usr/bin/xfconf-query -c '
                                               'xfce4-desktop -l | grep '
                                               '"workspace0/last-image"',
                                               shell=True).split()#nosec, rewrite
            for i in mon_list:
                subprocess.call(['/usr/bin/xfconf-query',#nosec
                                 '--channel', 'xfce4-desktop', '--property',
                                 i, '--set', file_name])

        elif self.desktop_environment == ('mate\n' or 'lightdm-xsession'): #experimental
            subprocess.run(['/usr/bin/gsettings', 'set', # nosec wont fix
                            'org.mate.background', 'picture-filename',
                            file_name])

        elif self.desktop_environment == 'gnome\n': #experimental
            subprocess.run(['/usr/bin/gsettings', 'set',#nosec wont fix
                            'org.gnome.desktop.background',
                            'picture-uri', '"file://' + file_name + '"'])

        elif self.desktop_environment == 'cinnamon2d\n':
            subprocess.run(['/usr/bin/gsettings', 'set',#nosec wont fix
                            'org.cinnamon.desktop.background',
                            'picture-uri', '"file://' + file_name + '"'])

        elif self.desktop_environment == 'i3\n':
            subprocess.run(['/usr/bin/feh', '--bg-scale', file_name]) 

        elif self.desktop_environment == 'Windows':
            # this is windows specific stuff
            # here we update our "online" wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20, 0, file_name, 0)
            # and here we update our registry with power shell
            # will it work on win7? who knows
            subprocess.call(['powershell', 'Set-ItemProperty', '-path',
                             '\'HKCU:\\Control Panel\\Desktop\\\'', '-name',
                             'wallpaper', '-value', file_name])
            subprocess.call(['rundll32.exe',
                             'user32.dll,', 'UpdatePerUserSystemParameters'])

    # def change_option(self, name, add=False): # DAFUCK
    #     '''need to rewrite it'''
    #     self.filer.change_option(name, add)

    def get_url(self):
        '''requests new link for wallpaper'''
        params = []
        if self.filer.settings['categories']:
            print(self.filer.settings['categories'])
            cat = random.choice(list(self.filer.settings['categories'].keys()))# nosec
            sub_cat = random.choice(self.filer.settings['categories'][cat])# nosec
            params.append(("category", cat))
            params.append(('sub_category', sub_cat))
        if not params:
            params = {}
        answer = get(self.api + '/walls', params=params)
        result = answer.json()
        if answer.status_code == 200:
            print(params)
        else:
            print('here the params', params)
            if answer.status_code == '404':
                print('SERVER ANSWERS 404 ON', answer.url)
            if answer.status_code == '403':
                print('SERVER ANSWERS 403 ON', answer.url)
            result = answer.status_code
        return result

    # def get_settings(self): # DAFUCKKK
    #     '''gets list of settings'''
    #     return self.filer.settings

    def get_categories(self):
        '''gets a list of all categories by api method'''
        params = {"categories":""}
        req = get(self.api, params=params).json()
        ong = []
        for i in req['categories']:
            ong.append(i + '::cat_')
            ong.append([l + '::sca_::' for l in req['categories'][i]])
        return ong

    def get_categories_as_dict(self):
        params = {"categories":""}
        request = get(self.api, params=params).json()
        return request['categories']

    def _sync_categories(self):
        # get all categories from api
        # and add it to settings json
        new_cats = self.get_categories_as_dict()
        with self.prefs.open('r') as file:
            base = json.load(file)
        js = base['categories']
        for key, value in new_cats.items():
            if key not in js:
                js[key] = []
            for sub_cat in value:
                if sub_cat not in [i['name'] for i in js[key]]:
                    js[key].append({"name":sub_cat, "checked":False})
        with self.prefs.open('w') as file:
            json.dump(base, file)
        print(js)


class Filer(): # TODO rewrite to PAth
    '''Abstraction for files and settings'''
    def __init__(self):
        self.main_folder = main_folder

        if not os.path.exists(self.main_folder):
            print("can`t see "\
            + self.main_folder + " folder!")
            os.mkdir(self.main_folder)

        if not os.path.exists(self.main_folder):
            print('creating!' + self.main_folder)
            os.mkdir(self.main_folder)

        if not os.path.exists(self.main_folder+'/saved/'):
            print('creating!' + self.main_folder+'/saved/')
            os.mkdir(self.main_folder+'/saved/')
        print('checking options!')
        try:
            with open(self.settings_file, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            print('file not found! creating new one')
            self.settings = {'categories':{}, 'resolutions':[]}

    #TODO logger to file

'this is the core of walld, all functions should store here'
import json
import random
import os
import subprocess #nosec
import requests
import ctypes #MANY THANKS TO J.J AND MESKSR DUDES YOU SAVED MY BURNED UP ASS https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python

class Walld():
    '''this class represents almost all walld functions except trays one'''
    def __init__(self, api, main_folder):
        self.main_folder = main_folder
        self.filer = Filer(self.main_folder)
        self.api = api
        self.save_path = self.main_folder+'/saved/' + str(random.random())#nosec
        if os.name == 'nt': #here comes windows specific stuff
            self.desktop_environment = 'Windows'
        else:
            code = "/usr/bin/env | /usr/bin/grep DESKTOP_SESSION= \
            | /usr/bin/awk -F= '{print $2}'"
            self.desktop_environment = \
            subprocess.check_output(code, shell=True).decode('ascii')#nosec, redo
        if not os.path.exists(self.main_folder):
            print("can`t see "\
            + self.main_folder + " folder!")
            exit(1)
        print('class walld started!')

    def save_image(self, name=False):
        '''copy image to specific(if passed) folder or to standart
        self.save_path path'''
        if name:
            subprocess.run(['/usr/bin/cp', self.main_folder+'/temp.jpg', name]\
            , shell=False)#nosec
            print('saved at ' + name)
        else:
            subprocess.run(['/usr/bin/cp', self.main_folder+'/temp.jpg',\
             self.save_path], shell=False)#nosec wont fix
            print('saved at ' + self.save_path)

    def spin_dice(self):
        '''making a list of urls by accessing a db, than sets wall'''
        new_url = self.get_urls()['url']
        if new_url == (404 or 403): 
            print('API IS NOT RESPONDING CORRECTLY') # tell this to user
        else:# api on that state is working BUT is this url good?
            if check_url(new_url):
                self.set_wall(download(new_url,\
                self.main_folder+'/temp.jpg'))
            else:
                print('check_url function is failed, doing nothing!') #need to tell this to user and send me mail

    def set_wall(self, file_name):
        '''this is critical module, depending on de it sets walls'''
        if self.desktop_environment == 'xfce\n':
            mon_list = subprocess.check_output('/usr/bin/xfconf-query -c \
xfce4-desktop -l | grep "workspace0/last-image"', shell=True).split()#nosec, rewrite
            print(mon_list)
            for i in mon_list:
                print('here comes')
                subprocess.call(['/usr/bin/xfconf-query',#nosec wont fix
'--channel', 'xfce4-desktop', '--property', i, '--set', file_name])
        elif self.desktop_environment == 'mate\n': #experimental
            subprocess.run(['/usr/bin/gsettings', 'set',#nosec wont fix
 'org.mate.background', 'picture-filename', file_name])
        elif self.desktop_environment == 'gnome\n': #experimental
            subprocess.run(['/usr/bin/gsettings', 'set',#nosec wont fix
'org.gnome.desktop.background', 'picture-uri file://', file_name])#nosec wont fix
        elif self.desktop_environment == 'Windows':
            print(file_name)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, file_name , 0)
            print('there`s need to make powershell script')

    def change_option(self, name, add=False):
        '''need to rewrite it'''
        self.filer.change_option(name, add)

    def get_urls(self):
        '''requests new link for wallpaper'''
        params = []
        if self.filer.settings['categories']:
            print(self.filer.settings['categories'])
            cat = random.choice(list(self.filer.settings['categories'].keys()))
            sub_cat = random.choice(self.filer.settings['categories'][cat])
            params.append(("category", cat))
            params.append(('sub_category', sub_cat))
        if not params:
            params = [('random', '1')]
        answer = requests.get(self.api\
         + '/walls', params=params)
        json_answer = json.loads(answer.text)
        if json_answer['success']:
            print(params)
            result = json_answer['content']
        else:
            print('here the params', params)
            if answer.status_code == '404':
                print('SERVER ANSWERS 404 ON', answer.url)
            if answer.status_code == '403':
                print('SERVER ANSWERS 403 ON', answer.url)
            result = answer.status_code
        return result


    def get_settings(self):
        '''gets list of settings'''
        return self.filer.settings

    def get_categories(self):
        '''gets a list of all categories by api method'''
        params = {"param":"categories"}
        json_answer = json.loads(requests.get(self.api, params=params).text)
        ong = []
        for i in json_answer['content']:
            ong.append(i['category']+'::cat_')
            ong.append([l+'::sca_::'+ i['category']  for l in i['subs']])
        return ong

class Filer():
    '''Abstraction for files and settings'''
    def __init__(self, main_folder):
        self.main_folder = main_folder
        self.settings_file = self.main_folder + '/prefs.json'
        if not os.path.exists(self.main_folder):
            print('creating!' + self.main_folder)
            os.mkdir(self.main_folder)
        print('checking options!')
        try:
            with open(self.settings_file, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            print('file not found! creating new one')
            self.settings = {'categories':{}, 'resolutions':[]}
            self.dump()

    def change_option(self, name, add=False):
        '''works with options file'''
        if add:
            print('adding', name)
            #if 'cat_' in name:
            #    self.settings['categories'][name] = {}
            if 'res_' in name:
                self.settings['resolutions'].append(name)
            elif 'sca_' in name:
                if not name.split('::')[2] in self.settings['categories']:
                    self.settings['categories'][name.split('::')[2]]= []
                self.settings['categories'][name.split('::')[2]].append(name.split('::')[0])
        else:
            print('removing', name)
            if 'cat_' in name:
                self.settings['categories'].remove(name[1:])
            elif 'res_' in name:
                self.settings['resolutions'].remove(name[1:])
            elif 'sca_' in name:
                lst = name.split("::")
                self.settings['categories'][lst[2]].remove(lst[0][1:])
        del_list = []
        for i in self.settings['categories']:
            if not self.settings['categories'][i]:
                del_list.append(i)
        for i in del_list:
            del self.settings['categories'][i]
        self.dump()

    def dump(self):
        '''this function dumps settings to file'''
        with open(self.settings_file, 'w') as temp:
            json.dump(self.settings, temp)

def download(url, file_name):
    '''downloads a file, first comes url, second comes full path of file'''
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    return file_name

def check_url(url):
    bad_codes = [404, 403, 501]
    ll = requests.get(url).status_code
    if ll in bad_codes:
        return False
    else:
         return True
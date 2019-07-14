import requests, json, random, os, sys, config, pickle, sqlite3

def get_categories():
    list = []
    params = {'auth':config.KEY, "method":"category_list"}
    r = json.loads(requests.get(config.API, params=params).text)
    for i in r['categories']:
        if i['name'] != 'Abstract':
            list.append('!' + i['name'] + '::cat_')
        else:
            list.append(i['name'] + '::cat_')
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
    '''this class represents almost all walld functions except trays one'''
    def __init__(self):
        if not os.path.exists(config.MAIN_FOLDER):
            print("This installation is incorrect! can`t see " + config.MAIN_FOLDER\
            + " folder!", file=sys.stderr)
            exit(1)
        print('class walld started!')

    def current_image(self, store = False):
        #сохранить бы в файл если честно
        if store:
            self.var = store
        else:
            return self.var

    def save_image(self, name = False):
        if not name:
            self.save_path =  config.MAIN_FOLDER+'/saved/' + str(random.random())
        else:
            self.save_path = name
        os.system('cp ' + config.MAIN_FOLDER+'/temp.jpg ' + self.save_path)# имя бы достать
        print('saved at ' + self.save_path)

    def guess_de(self):
        pass#need to guess current de

    def get_settings(self):
        return filer.settings

    def add_option(self, name): # не очень это красиво, брат
        filer.change_option(name, add = True)

    def remove_option(self, name):
        filer.change_option(name)

    def spin_dice(self, chance):
        list = []
        for i in range(0, 20):
            PARAMS = {'auth':config.KEY, "method":"category",'id':'1',
            'page':i, 'width': '1920',
            'height':'1080', 'operator':'min'}
            r = json.loads(requests.get(config.API, params=PARAMS).text)
            print('getting ', i)
            if r['success']:
                if r['wallpapers']:
                    list += r['wallpapers']
                else:
                    print('breaking!')
                    break
            else:
                print('whoops')
        for i in list:
            key = random.randint(0, 100)
            if key >= chance:
                print('ok, key is ' + str(key) +'\nPrinting out wall')
                print('downloading', i['url_image'], '...', end = ' ')
                download(i['url_image'], config.MAIN_FOLDER+'/temp.jpg')
                print('ok!')#узнать бы как это более централизованно сделать
                set_wall(config.MAIN_FOLDER+'/temp.jpg')
                break
            else:
                print('pass, key was '+ str(key))
        else:
            pass

class Filer:
    '''Abstraction for files and settings'''
    def __init__(self, db_name):
        self.db_name = db_name
        print('filer class is started, checking db!')
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM pics")
            print('found db!')
        except sqlite3.OperationalError:
            print('need to download db!')
            download(config.DB_URL, config.DB_NAME)
            print('ok!')
        print('checking options!')
        try:
            with open(config.SETTINGS_FILE, 'rb') as file:
                self.settings = pickle.load(file)
        except FileNotFoundError:
            print('file not found! creating new one')
            self.settings = []
            self.dump()

    def dump(self):
        with open(config.SETTINGS_FILE, 'wb') as temp:
            pickle.dump(self.settings, temp)

    def change_option(self, name, add = False):
        print(filer.settings)
        if add:# прописать pickle
            print('adding', name)
            self.settings.append(name)
        else:
            print('removing', name)
            self.settings.remove(name)
        self.dump()

filer = Filer(config.DB_NAME)

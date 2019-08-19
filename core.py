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
    return file_name


def set_wall(file_name):
    de = os.popen("env | grep DESKTOP_SESSION= | awk -F= '{print $2}'").read()
    print('this is de' + de)
    if de == 'xfce\n':
        mon_list = os.popen('/usr/bin/xfconf-query -c \
        xfce4-desktop -l | grep "workspace0/last-image"').read().split()
        for i in mon_list:
            os.system('xfconf-query \
            --channel xfce4-desktop --property '+ i +' --set ' + file_name)
    elif de == 'mate\n': #experimental
        os.system('/usr/bin/gsettings set org.mate.background\
         picture-filename'+ file_name)
    elif de == 'gnome\n': #experimental
        os.system('/usr/bin/gsettings set \
        org.gnome.desktop.background picture-uri file://'+ file_name)

class Walld(object):
    '''this class represents almost all walld functions except trays one'''
    def __init__(self):
        if not os.path.exists(config.MAIN_FOLDER):
            print("This installation is incorrect! can`t see "
            + config.MAIN_FOLDER
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


    def get_settings(self):
        return filer.settings

    def add_option(self, name): # не очень это красиво, брат
        filer.change_option(name, add = True)

    def remove_option(self, name):
        filer.change_option(name)

    def spin_dice(self, chance):
        l = []
        for i in filer.get_urls('abstract'):# нужно дергать настройки дабы узнать че дергать
            l.append(i[4])
        set_wall(download(random.choice(l),config.MAIN_FOLDER+'/temp.jpg'))

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

    def dump(self):
        with open(config.SETTINGS_FILE, 'wb') as temp:
            pickle.dump(self.settings, temp)

    def get_urls(self, category):
        self.sql = "SELECT * FROM pics WHERE category='Abstract'"
        self.cursor.execute(self.sql)
        return self.cursor.fetchall()

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

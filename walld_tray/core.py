"""
This is the core of walld client code,
all functions related to:
 - working with settings
 - making requests to api
 = working with files
should store here
"""
import ctypes  # MANY THANKS TO J.J AND MESKSR DUDES YOU SAVED MY BURNED UP ASS
import json
import os
import random
import shutil
import subprocess
from pathlib import Path

from requests import get

from helpers import download, DesktopEnvironment

#  stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python

MAIN_FOLDER = Path().home() / '.walld'
URL_LOG = MAIN_FOLDER / 'walld.log'  # get it from settings!


class Walld:
    """
    Class that works with walls and save files
    Its doesnt matter which DE is useed, this
    class provides abstraction for that
    """

    def __init__(self, api, main_folder=MAIN_FOLDER):
        self.main_folder = main_folder
        self.api = api
        self.prefs_path = self.main_folder / 'prefs.json'
        self.categories = self.prefs.get('categories')
        self._sync_categories()
        self.de = DesktopEnvironment()
        self.connected = True

        # self.save_path = (self.main_folder+'/saved/' +
        #                   str(random.random()) + '.png')#nosec

        self._sync_categories()
        # print('class walld started!')
        # log.info class walld started

    def save_image(self, name=None):
        """
        Copy image to specific(if passed)
        folder or to standart
        self.save_path path
        """
        if name:
            shutil.copyfile(self.main_folder_temp, name)  # nosec
            print('saved at ' + name)

        else:
            shutil.copyfile(self.main_folder_temp, self.save_path)  # nosec wont fix
            print('saved at ' + self.save_path)
            self.save_path = (f'{self.main_folder}/saved/'
                              f'{str(random.random())}.png')  # nosec

    def set_wall_from_api(self):  # TODO rename
        """making a list of urls by accessing a db, than sets wall"""
        url = self.get_url()['url']
        # log.info(url)
        file_name = download(url, self.main_folder / 'temp.jpg')
        self.de.set_wall(file_name)

    # def _get_checked_categories(self):
    #     result = []
    #     for category in self.categories:
    #         for sub_category in category:
    #             if sub_category["checked"]:

    def get_url(self):  # TODO REDO
        """
        Requests new link for wallpaper
        """
        params = []
        #  Get checked categories
        if self.filer.settings['categories']:
            print(self.filer.settings['categories'])
            cat = random.choice(list(self.filer.settings['categories'].keys()))  # nosec
            sub_cat = random.choice(self.filer.settings['categories'][cat])  # nosec
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

    @property
    def _api_get_categories(self):
        """
        Using get method gets(from API)
        dict of categories
        """
        params = {"categories": ""}
        request = get(self.api, params=params).json()
        return request['categories']

    @property
    def prefs(self):
        base_settings = dict(categories=dict(), system=dict(), tags=dict())
        if not self.prefs_path.exists():
            return base_settings

        with self.prefs_path.open('r') as file:
            loaded_prefs = json.load(file)

        if loaded_prefs.keys() != base_settings.keys():
            return base_settings
        return loaded_prefs

    @prefs.setter
    def prefs(self, value):
        with self.prefs_path.open('w') as file:
            json.dump(file, value)

    # @property
    # def categories(self):
    #     return self.prefs['categories']

    # @categories.setter
    # def categories(self, value):
    #     with self.prefs_path.open('w') as file:

    def _sync_categories(self):
        """
        Update self categories
        with new one`s from api if any
        and dump it to settings json
        """
        for key, value in self._api_get_categories.items():
            if key not in self.categories:
                self.categories[key] = []

            for sub_cat in value:
                if sub_cat not in [i['name'] for i in self.categories[key]]:
                    sub_category_prefs = dict(name=sub_cat, checked=False)
                    self.categories[key].append(sub_category_prefs)

        with self.prefs_path.open('w') as file:
            json.dump(self.categories, file)


class Filer():  # TODO rewrite to PAth
    '''Abstraction for files and settings'''

    def __init__(self):
        self.main_folder = main_folder

        if not os.path.exists(self.main_folder):
            print("can`t see " \
                  + self.main_folder + " folder!")
            os.mkdir(self.main_folder)

        if not os.path.exists(self.main_folder):
            print('creating!' + self.main_folder)
            os.mkdir(self.main_folder)

        if not os.path.exists(self.main_folder + '/saved/'):
            print('creating!' + self.main_folder + '/saved/')
            os.mkdir(self.main_folder + '/saved/')
        print('checking options!')
        try:
            with open(self.settings_file, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            print('file not found! creating new one')
            self.settings = {'categories': {}, 'resolutions': []}

    # TODO logger to file

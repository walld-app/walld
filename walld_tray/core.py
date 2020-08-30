"""
This is the core of walld client code,
all functions related to:
 - working with settings
 - making requests to api
 = working with files
should store here
"""

import json
import shutil
from pathlib import Path
from random import choice
from typing import Optional
from uuid import uuid4

from requests import get

from helpers import DesktopEnvironment, download

#  stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python

MAIN_FOLDER = Path().home() / '.walld'
URL_LOG = MAIN_FOLDER / 'walld.log'  # get it from settings!


class Walld:
    """
    Class that works with walls, api and also save files
    It doesnt matter which DE is used, this
    class contains abstraction for that
    """

    def __init__(self, api, main_folder=MAIN_FOLDER):
        self.main_folder = main_folder
        self.api = api
        self.prefs_path = self.main_folder / 'prefs.json'
        self.prefs_in_mem = self.prefs  # TODO REDO
        self.save_path = self.main_folder / 'saved'
        self.temp_wall = self.main_folder / 'temp.jpg'
        self.categories = self.prefs.get('categories')
        self._sync_categories()
        self.de = DesktopEnvironment()
        self.connected = True
        # log.debug('class walld started')

    def save_image(self, path: Optional[Path] = None):
        """
        Copy image to specific(if passed)
        folder or to standard
        self.save_path path
        """
        if not path:
            path = self.save_path / f"{str(uuid4())}.png"

        shutil.copyfile(self.temp_wall, path)  # nosec wont fix
        # log.info(f"saved at {path}")  # TODO

    def set_wall(self):  # TODO rename
        """making a list of urls by accessing a db, than sets wall"""
        url = self.get_url()['url']
        # log.info(url)
        file_name = download(url, self.main_folder / 'temp.jpg')
        self.de.set_wall(file_name)

    def _get_checked_categories(self):
        result = {}
        for category in self.categories:
            for sub_category in self.categories[category]:
                if sub_category["checked"]:
                    if not result.get(category):
                        result[category] = []
                    result[category].append(sub_category["name"])
        return result

    def get_url(self):  # TODO api talker decorator
        """
        Requests new link for wallpaper
        """
        params = dict()
        if self.categories:
            checked_cats = self._get_checked_categories()
            cat = choice(list(checked_cats.keys()))
            sub_cat = choice(checked_cats[cat])
            params = dict(category=cat, sub_category=sub_cat)

        answer = get(self.api + '/walls', params=params)
        return answer.json()

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
        pretty_json = json.dumps(value, indent=2)
        with self.prefs_path.open('w') as file:
            file.write(pretty_json)

    def _sync_categories(self):
        """
        Update self categories
        with new one`s from api if any
        Dump them to settings json file
        """
        api_categories = self._api_get_categories.items()

        for key in list(self.categories.keys()):
            if key not in api_categories:
                del self.categories[key]

        for key, value in api_categories:
            if key not in self.categories:
                self.categories[key] = []

            for sub_cat in value:
                if sub_cat not in [i['name'] for i in self.categories[key]]:
                    sub_category_prefs = dict(name=sub_cat, checked=False)
                    self.categories[key].append(sub_category_prefs)
        self.prefs_in_mem['categories'] = self.categories
        self.prefs = self.prefs_in_mem

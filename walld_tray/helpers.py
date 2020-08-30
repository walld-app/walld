# TODO 500/404 handler
import ctypes  # MANY THANKS TO J.J AND MESKSR DUDES YOU SAVED MY BURNED UP ASS
import platform
import subprocess
from pathlib import Path

import requests
from PyQt5 import QtCore, QtGui
from requests import get

from config import log


def api_talk_handler(function):  # TODO retry, exceptions for http errors
    def wrapper(*args, **kwargs):
        for _ in range(5):
            try:
                final = function(*args, **kwargs)
                return final
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.ConnectTimeout):
                print('Something is happening with server, trying again...')
        print('giving up')
    return wrapper


def download(url: str, file_name: Path) -> Path:
    """
    Downloads file to specified location
    :param url: url of file
    :param file_name filepath WITH name to save
    """
    try:
        response = get(url)
    except requests.exceptions.ConnectionError:
        url = url.replace('s', '', 1)
        response = get(url)

    with open(file_name, "wb") as file:
        file.write(response.content)
    return file_name


def clear_layout(layout):
    """
    Clears qt layout from widgets
    """
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().hide()


def b64_to_icon(base64: bytes) -> QtGui.QIcon:
    """
    Converts base64 code to QtGui icon
    """
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon


class DesktopEnvironment:
    def __init__(self):
        self.name: str
        self.current_wallpaper: str  # not implemented
        self._detect_desktop_environment()
        log.debug(f"DE - {self.name}")

    def _detect_desktop_environment(self):
        if platform.system() == 'Windows':  # Here comes windows specific stuff
            self.name = platform.system().lower()

        else:
            code = ("/usr/bin/env | /usr/bin/grep DESKTOP_SESSION= "
                    "| /usr/bin/awk -F= '{print $2}'")
            self.name = subprocess.check_output(code, shell=True).decode('ascii').rstrip().lower()

    def set_wall(self, file_name: Path):
        """
        Function that, depending on DE, sets walls'''
        """
        if self.name == 'xfce':
            mon_list = subprocess.check_output('/usr/bin/xfconf-query -c '
                                               'xfce4-desktop -l | grep '
                                               '"workspace0/last-image"',
                                               shell=True).split()  # nosec, rewrite
            for i in mon_list:
                subprocess.call(['/usr/bin/xfconf-query',  # nosec
                                 '--channel', 'xfce4-desktop', '--property',
                                 i, '--set', file_name])

        elif self.name == ('mate' or 'lightdm-xsession'):  # experimental
            subprocess.run(['/usr/bin/gsettings', 'set',  # nosec wont fix
                            'org.mate.background', 'picture-filename',
                            file_name])

        elif self.name == 'gnome':  # experimental
            subprocess.run(['/usr/bin/gsettings', 'set',  # nosec wont fix
                            'org.gnome.desktop.background',
                            'picture-uri', '"file://' + file_name + '"'])

        elif self.name == 'cinnamon2d':
            subprocess.run(['/usr/bin/gsettings', 'set',  # nosec wont fix
                            'org.cinnamon.desktop.background',
                            'picture-uri', '"file://' + file_name + '"'])

        elif self.name == 'i3':
            subprocess.run(['/usr/bin/feh', '--bg-scale', file_name])

        elif self.name == 'windows':
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
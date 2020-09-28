# TODO 500/404 handler
import ctypes  # MANY THANKS TO J.J AND MESKSR DUDES YOU SAVED MY BURNED UP ASS
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from time import sleep

import requests
from PyQt5 import QtCore, QtGui
from requests import get

from config import log


def retry(function, count: int = 3, interval: int = 0.1):
    def wrapper(*args, **kwargs):
        range_ = list(range(1, count+1))[::-1]
        error: Exception
        for num in range_:
            try:
                final = function(*args, **kwargs)
                return final
            except Exception as e:
                error = e
                log.error(f'Attempt - {num}/{count}\n'
                          f'Retrying after exception {str(e)}')
                sleep(interval)
        log.fatal(f'Giving up after {count} retries')
        raise error
    return wrapper


@retry
def download(url: str, file_name: Path) -> Path:
    """
    Downloads file to specified location
    :param url: url of file
    :param file_name filepath WITH name to save
    """
    try:
        url = url.replace('s', '', 1)
        response = get(url)
    except requests.exceptions.ConnectionError:
        response = get(url)

    finally:
        if response.status_code != 200:
            raise

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


@dataclass
class DETools:
    i3 = 'feh'
    gnome = 'gsettings'
    xfce = 'xfconf-query'
    mate = gnome
    cinnamon2d = gnome
    lightdm_xsession = gnome
    windows = 'powershell'


class DesktopEnvironment:
    def __init__(self):
        self.name: str
        self.current_wallpaper: str  # not implemented
        self.pywal_presented = False
        self._detect_desktop_environment()
        self.tool_path: Path
        self._find_tools()
        log.debug(f"DE - {self.name}, Tool - {str(self.tool_path)}")

    def _find_tools(self):
        try:
            import pywall
        except ImportError:
            pass
        else:
            self.pywal_presented = True

        tool_path = which(getattr(DETools, self.name.replace('-', '_')))

        if not tool_path:
            raise FileNotFoundError(f'cant file binary for changing walls!')

        self.tool_path = tool_path

    def _detect_desktop_environment(self):
        if platform.system() == 'Windows':  # Here comes windows specific stuff
            self.name = platform.system().lower()

        else:
            code = (f"{which('env')} | {which('grep')} DESKTOP_SESSION= | {which('awk')} -F= "
                    "'{print $2}'")
            self.name = subprocess.check_output(code, shell=True).decode('ascii').rstrip().lower()

    def set_wall(self, file_name: Path, apply_theme: bool = False):
        """
        Function that, depending on DE, sets walls'''
        """
        if apply_theme and self.pywal_presented:
            # pywall stuff
            pass

        if self.name == 'xfce':
            mon_list = subprocess.check_output(f'{self.tool_path} -c '
                                               'xfce4-desktop -l | grep '
                                               '"workspace0/last-image"',
                                               shell=True).split()  # nosec, rewrite
            for i in mon_list:
                subprocess.call([self.tool_path,  # nosec
                                 '--channel', 'xfce4-desktop', '--property',
                                 i, '--set', file_name])

        elif self.name in ('mate', 'lightdm-xsession'):  # experimental
            subprocess.run([self.tool_path, 'set',  # nosec wont fix
                            'org.mate.background', 'picture-filename',
                            file_name])

        elif self.name == 'gnome':  # experimental
            subprocess.run([self.tool_path, 'set',  # nosec wont fix
                            'org.gnome.desktop.background',
                            'picture-uri', '"file://' + file_name + '"'])

        elif self.name == 'cinnamon2d':
            subprocess.run([self.tool_path, 'set',  # nosec wont fix
                            'org.cinnamon.desktop.background',
                            'picture-uri', '"file://' + file_name + '"'])

        elif self.name == 'i3':
            subprocess.run([self.tool_path, '--bg-center', file_name])

        elif self.name == 'windows':
            # this is windows specific stuff
            # here we update our "online" wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20, 0, file_name, 0)
            # and here we update our registry with power shell
            # will it work on win7? who knows
            subprocess.call(['powershell', 'Set-ItemProperty', '-path',
                             '\'HKCU:\\Control Panel\\Desktop\\\'', '-name',
                             'wallpaper', '-value', file_name])
            subprocess.call([which('rundll32.exe'),
                             'user32.dll,', 'UpdatePerUserSystemParameters'])

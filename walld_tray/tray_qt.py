from sys import argv

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QSystemTrayIcon

from .config import API, ICON
from .core import Walld

app = QApplication(argv)
app.setQuitOnLastWindowClosed(False)
walld = Walld(API, MAIN_FOLDER)


def b64_to_icon(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    ico = QtGui.QIcon(pixmap)
    return ico


icon = QIcon(b64_to_icon(ICON))

tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# def gen_menu():
#     cats = walld.get_categories_as_dict()
#     print(cats)
#     categories_menu = QMenu('Categories')
#     c = []
#     for category in cats:
#         action = QAction(category)
#         action.triggered.connect(lambda chk, cat=category: print(cat))
#         c.append(action)
#     categories_menu.addActions(c)
#     return categories_menu

menu = QMenu()

shut_down = QAction("Quit")
shut_down.triggered.connect(app.quit)

change_wallpaper = QAction("Change wallpaper")
change_wallpaper.triggered.connect(walld.set_wall_from_api)
settings = QAction("Settings")
# change_wallpaper.triggered.connect(_
# cates = gen_menu()

menu.addAction(change_wallpaper)
menu.addAction(settings)
menu.addAction(shut_down)
tray.setContextMenu(menu)

app.exec_()

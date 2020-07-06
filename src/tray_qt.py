from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from config import ICON, API, MAIN_FOLDER
from core import Walld
from sys import argv

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

menu = QMenu()

shut_down = QAction("Quit")
shut_down.triggered.connect(app.quit)

change_wallpaper = QAction("Change wallpaper")
change_wallpaper.triggered.connect(walld.spin_dice)

menu.addAction(change_wallpaper)
menu.addAction(shut_down)


tray.setContextMenu(menu)

app.exec_()

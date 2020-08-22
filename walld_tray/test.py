import sys
from functools import partial

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMenu, QPushButton,
                             QWidget, QSpacerItem, QSizePolicy, QSystemTrayIcon
                             )
from core import Walld
from config import API, ICON
from PyQt5.QtCore import QSize
from pathlib import Path
from helpers import b64_to_icon, clear_layout

TEMPLATE_DIR = Path('.') / "template"


class CategoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(TEMPLATE_DIR / "category_widget.ui", self)


class Ui(QMainWindow):
    def __init__(self, walld, icon: QtGui.QIcon):
        super().__init__()
        uic.loadUi(TEMPLATE_DIR / "settings.ui", self)  # Load the .ui file
        #  self.show()  # Show the GUI
        self.category_widget = CategoryWidget()
        self.walld = walld
        self.icon = icon
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self.categories = self.walld.get_categories_as_dict()
        self._gen_categories_buttons()
        self.RightMenu.addWidget(self.category_widget)
        self.category_widget.hide()

    def _gen_categories_buttons(self):
        self.cats_buttons = {}
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        for i in self.categories:
            ll = QPushButton(i)
            ll.setMinimumSize(QSize(0, 40))
            self.cats_buttons[i] = {'category': ll, 'sub_categories': []}
            # make for loop for iterating over sub categ
            for l in self.categories[i]:
                sub_category_button = QPushButton(l)
                sub_category_button.setMinimumSize(QSize(0, 40))
                sub_category_button.setCheckable(True)
                self.cats_buttons[i]['sub_categories'].append(sub_category_button)
                self.category_widget.SubCategoriesLayout.addWidget(sub_category_button)
                sub_category_button.hide()
            self.category_widget.CategoriesLayout.addWidget(ll)
        self.category_widget.SubCategoriesLayout.addSpacerItem(spacer)
        self.category_widget.CategoriesLayout.addSpacerItem(spacer)

    def bring_sub_categories(self, category):
        self.hide_buttons('sub_categories')
        for i in self.cats_buttons[category]['sub_categories']:
            i.show()

    def hide_buttons(self, category):
        print(self.cats_buttons, 'shiet')
        for l in self.cats_buttons:
            for i in self.cats_buttons[l].get(category, []):
                i.hide()


class UiCtrl:
    """Ui Controller class."""
    def __init__(self, view, walld):
        """Controller initializer."""
        self.view = view
        self.walld = walld
        # Connect signals and slots
        self._connect_signals()

    def _connect_signals(self):
        """Connect signals and slots."""
        self.view.ColourButton.clicked.connect(self.view.category_widget.show)
        self.view.CategoriesButton.clicked.connect(self.view.category_widget.show)
        self.view.TagButton.clicked.connect(partial(clear_layout, self.view.RightMenu))
        for i in self.view.cats_buttons:
            i = self.view.cats_buttons[i]['category']
            i.clicked.connect(partial(self.view.bring_sub_categories, i.text()))


if __name__ == "__main__":

    walld_core = Walld(API)  # TODO Exception for not connecting
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    icon = b64_to_icon(ICON)
    window = Ui(walld_core, icon)
    UiCtrl(window, walld_core)

    menu = QMenu()
    shut_down = QAction("Quit")
    shut_down.triggered.connect(app.quit)

    change_wallpaper = QAction("Change wallpaper")
    # change_wallpaper.triggered.connect(walld.spin_dice)
    settings = QAction("Settings")
    settings.triggered.connect(window.show)

    menu.addAction(change_wallpaper)
    menu.addAction(settings)
    menu.addAction(shut_down)
    window.tray.setContextMenu(menu)

    app.exec_()

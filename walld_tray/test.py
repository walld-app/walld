import sys
from functools import partial
from typing import Any, Union

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMenu, QPushButton,
                             QWidget, QSpacerItem, QSizePolicy, QSystemTrayIcon
                             )
from core import Walld
from config import API, ICON
from PyQt5.QtCore import QSize
from pathlib import Path
from helpers import b64_to_icon, clear_layout

TEMPLATE_DIR: Union[Path, Any] = Path('.') / "template"


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
        self.walld = walld  # TODO it will crash if walld is not connected to a service
        self.icon = icon
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self._gen_categories_buttons()
        self.RightMenu.addWidget(self.category_widget)
        self.category_widget.hide()

    def _gen_categories_buttons(self):
        self.cats_buttons = {}
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        for i in self.walld.categories:
            ll = QPushButton(i)
            ll.setMinimumSize(QSize(0, 40))
            self.cats_buttons[i] = dict(category=ll, sub_categories=[])
            # make for loop for iterating over sub category
            for sub_category in self.walld.categories[i]:
                sub_category_button = QPushButton(sub_category['name'])
                sub_category_button.setMinimumSize(QSize(0, 40))
                sub_category_button.setCheckable(True)
                sub_category_button.setChecked(sub_category['checked'])
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
        for button in self.cats_buttons:
            for i in self.cats_buttons[button].get(category, []):
                i.hide()

    def check_button(self, category, button):  # TODO REDO
        for num, i in enumerate(self.walld.prefs_in_mem['categories'][category]):
            if i['name'] == button.text():
                self.walld.prefs_in_mem['categories'][category][num]['checked'] = button.isChecked()
                break

        self.walld.prefs = self.walld.prefs_in_mem


class UiCtrl:
    """Ui Controller class."""
    def __init__(self, view):
        """Controller initializer."""
        self.view = view
        # Connect signals and slots
        self._connect_signals()

    def _connect_signals(self):
        """Connect signals and slots."""
        self.view.ColourButton.clicked.connect(self.view.category_widget.show)
        self.view.CategoriesButton.clicked.connect(self.view.category_widget.show)
        self.view.TagButton.clicked.connect(partial(clear_layout, self.view.RightMenu))

        for i in self.view.cats_buttons:
            button = self.view.cats_buttons[i]['category']
            button.clicked.connect(partial(self.view.bring_sub_categories, button.text()))
            sub_categories_buttons = self.view.cats_buttons[i]['sub_categories']
            for sc_button in sub_categories_buttons:
                sc_button.clicked.connect(partial(self.view.check_button, button.text(), sc_button))


if __name__ == "__main__":
    walld_core = Walld(API)  # TODO Exception for not connecting
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Ui(walld_core, b64_to_icon(ICON))
    UiCtrl(window)

    menu = QMenu()
    shut_down = QAction("Quit")
    shut_down.triggered.connect(app.quit)

    change_wallpaper = QAction("Change wallpaper")
    change_wallpaper.triggered.connect(walld_core.set_wall)
    settings = QAction("Settings")
    settings.triggered.connect(window.show)

    menu.addAction(change_wallpaper)
    menu.addAction(settings)
    menu.addAction(shut_down)
    window.tray.setContextMenu(menu)

    app.exec_()

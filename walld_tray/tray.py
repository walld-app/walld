import sys
from functools import partial
from pathlib import Path
from typing import Any, Union

from PyQt5 import QtGui, uic
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMenu, QPushButton, QSizePolicy, QSpacerItem,
                             QSystemTrayIcon, QWidget, QFileDialog
                             )

from config import API, ICON
from core import Walld
from helpers import b64_to_icon, clear_layout

TEMPLATE_DIR: Union[Path, Any] = Path('.') / "template"


class CategoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(TEMPLATE_DIR / "category_widget.ui", self)


class SettingsSystem(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(TEMPLATE_DIR / "settings_system.ui", self)


class Ui(QMainWindow):
    def __init__(self, walld: Walld, icon: QtGui.QIcon):
        super().__init__()
        uic.loadUi(TEMPLATE_DIR / "settings.ui", self)
        self.category_widget = CategoryWidget()
        self.setting_system = SettingsSystem()
        self.walld = walld
        self.icon = icon
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self._gen_categories_buttons()
        self.RightMenu.addWidget(self.category_widget)
        self.RightMenu.addWidget(self.setting_system)
        self.category_widget.hide()
        self.setting_system.hide()

    def _gen_categories_buttons(self):
        self.cats_buttons = {}
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        for i in self.walld.categories:

            ll = QPushButton(i)
            ll.setMinimumSize(QSize(0, 40))

            self.cats_buttons[i] = dict(category=ll, sub_categories=[])

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
        if len(str(self.walld.download_path)) > 65:
            self.setting_system.folder_path.setText(f'{str(self.walld.download_path)[:65]}...')
        else:
            self.setting_system.folder_path.setText(str(self.walld.download_path))

    def bring_sub_categories(self, category):
        self.hide_buttons('sub_categories')
        for i in self.cats_buttons[category]['sub_categories']:
            i.show()

    def show_(self, widget: QWidget):
        clear_layout(self.RightMenu)
        widget.show()

    def hide_buttons(self, category):
        for button in self.cats_buttons:
            for i in self.cats_buttons[button].get(category, []):
                i.hide()

    def check_button(self, category, button):  # TODO REDO
        for num, i in enumerate(self.walld.prefs_in_mem['categories'][category]):
            if i['name'] == button.text():
                self.walld.prefs_in_mem['categories'][category][num]['checked'] = button.isChecked()
                break

        self.walld.prefs_on_disk = self.walld.prefs_in_mem

    def folder_button(self):
        name = QFileDialog.getExistingDirectory(self, "Name the directory")
        if name:
            self.walld.prefs_in_mem['system']['download_path'] = name
            self.walld.dump_prefs()
            if len(name) > 65:
                name = f'{name[:65]}...'
            self.setting_system.folder_path.setText(name)


class UiCtrl:
    """Ui Controller class."""
    def __init__(self, view: Ui):
        """Controller initializer."""
        self.view = view
        # Connect signals and slots
        self._connect_signals()

    def _connect_signals(self):
        """Connect signals and slots."""
        self.view.ColourButton.clicked.connect(self.view.category_widget.show)
        self.view.CategoriesButton.clicked.connect(partial(self.view.show_, self.view.category_widget))
        self.view.TagButton.clicked.connect(partial(clear_layout, self.view.RightMenu))
        self.view.SystemButton.clicked.connect(partial(self.view.show_, self.view.setting_system))
        self.view.setting_system.choose_folder_button.clicked.connect(self.view.folder_button)

        for i in self.view.cats_buttons:
            button = self.view.cats_buttons[i]['category']
            button.clicked.connect(partial(self.view.bring_sub_categories, button.text()))
            sub_categories_buttons = self.view.cats_buttons[i]['sub_categories']
            for sc_button in sub_categories_buttons:
                sc_button.clicked.connect(partial(self.view.check_button, button.text(), sc_button))


def main():
    walld = Walld(API)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Ui(walld, b64_to_icon(ICON))
    UiCtrl(window)

    menu = QMenu()
    shut_down = QAction("Quit")
    shut_down.triggered.connect(app.quit)

    change_wallpaper = QAction("Change wallpaper")
    change_wallpaper.triggered.connect(walld.set_wall)
    settings = QAction("Settings")
    settings.triggered.connect(window.show)

    menu.addAction(change_wallpaper)
    menu.addAction(settings)
    menu.addAction(shut_down)
    window.tray.setContextMenu(menu)

    sys.exit(app.exec_())

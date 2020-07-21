import sys
from functools import partial

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QWidget, QSpacerItem, QSizePolicy)
from core import Walld
from config import API, MAIN_FOLDER
from PyQt5.QtCore import Qt, QSize


class CategoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/template/category_widget.ui', self)


class Ui(QMainWindow):
    def __init__(self, walld):
        super().__init__()
        uic.loadUi('src/template/settings.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.category_widget = CategoryWidget()
        self.walld = walld
        self.categories = self.walld.get_categories_as_dict()
        self._gen_categories_buttons()

    def _gen_categories_buttons(self):
        self.cats_buttons = []
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        for i in self.categories:
            ll = QPushButton(i)
            ll.setMinimumSize(QSize(0, 40))
            self.cats_buttons.append(ll)
            self.category_widget.CategoriesLayout.addWidget(ll)
        self.category_widget.CategoriesLayout.addSpacerItem(spacer)
        # print(dir(self.category_widget.SubCategoriesLayout))
        print(self.cats_buttons)

    def bring_categories(self):
        self.clear_layout(self.RightMenu)
        self.RightMenu.addWidget(self.category_widget)
        # self.clear_layout(self.category_widget.verticalLayout_2)

    def bring_sub_categories(self, category):
        print(category)
        clearLayout(self.category_widget.SubCategoriesLayout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        for i in self.categories[category]:
            ll = QPushButton(i)
            ll.setMinimumSize(QSize(0, 40))
            ll.setCheckable(True)
            self.category_widget.SubCategoriesLayout.addWidget(ll)
        self.category_widget.SubCategoriesLayout.addSpacerItem(spacer)

    def clear_layout(self, layout):
        print('clear')
        # layout = self.RightMenu
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)


class UiCtrl:
    """Ui Controller class."""
    def __init__(self, view, walld):
        """Controller initializer."""
        self.view = view
        self.walld = walld
        # Connect signals and slots
        self._connectSignals()

    def _connectSignals(self):
        """Connect signals and slots."""
        self.view.ColourButton.clicked.connect(self.view.bring_categories)
        self.view.CategoriesButton.clicked.connect(self.view.bring_categories)
        self.view.TagButton.clicked.connect(partial(self.view.clear_layout, self.view.RightMenu))
        for i in self.view.cats_buttons:
            print(i.text())
            i.clicked.connect(partial(self.view.bring_sub_categories, i.text()))

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

walld = Walld(API, MAIN_FOLDER)
app = QApplication(sys.argv)
window = Ui(walld)
UiCtrl(window, walld)
app.exec_()

import sys
from functools import partial

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QWidget, QSpacerItem, QSizePolicy)
from src.core import Walld
from src.config import API
from PyQt5.QtCore import QSize


class CategoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/template/category_widget.ui', self)


def clear_layout(layout):
    # layout = self.RightMenu
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().hide()


class Ui(QMainWindow):
    def __init__(self, walld):
        super().__init__()
        uic.loadUi('src/template/settings.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.category_widget = CategoryWidget()
        self.walld = walld
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
        # self.clear_layout(self.category_widget.SubCategoriesLayout)
        self.hide_buttons('sub_categories')
        for i in self.cats_buttons[category]['sub_categories']:
            # self.category_widget.SubCategoriesLayout.addWidget(i)
            # ll = QPushButton(i)
            # ll.setMinimumSize(QSize(0, 40))
            # ll.setCheckable(True)
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
        self.view.TagButton.clicked.connect(partial(self.view.clear_layout, self.view.RightMenu))
        for i in self.view.cats_buttons:
            i = self.view.cats_buttons[i]['category']
            i.clicked.connect(partial(self.view.bring_sub_categories, i.text()))


# def clearLayout(layout):
#     while layout.count():
#         child = layout.takeAt(0)
#         if child.widget() is not None:
#             child.widget().deleteLater()
#         elif child.layout() is not None:
#             clearLayout(child.layout())

walld_core = Walld(API)  # TODO Exception for not connecting
app = QApplication(sys.argv)
window = Ui(walld_core)
UiCtrl(window, walld_core)
app.exec_()

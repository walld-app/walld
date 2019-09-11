#!/usr/bin/python3
import core
import gi
import config
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

walld = core.Walld(config.API, config.MAIN_FOLDER)

class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.set_from_icon_name('help-about')
        self.connect("popup_menu", self.on_secondary_click)

    def on_secondary_click(self, widget, button, time):
        menu = Gtk.Menu()
        submenu = Gtk.Menu()

        menu_item1 = Gtk.MenuItem(label = "First Entry", submenu= submenu)
        mi3 = Gtk.MenuItem(label = "spin_dice")
        mi3.connect('activate', walld.spin_dice)

        menu_item2 = Gtk.MenuItem(label = "Quit")
        menu_item2.connect('activate', Gtk.main_quit)
        menu.append(mi3)
        menu.append(menu_item1)
        submenu.append(menu_item2)

        menu.show_all()
        menu.popup(None, None, None, self, 4, time)

if __name__ == '__main__':
    tray = TrayIcon()

    Gtk.main()

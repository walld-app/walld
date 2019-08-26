#!/usr/bin/python3
import core
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

walld = core.Walld()

class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.set_from_icon_name('help-about')
        self.connect("popup_menu", self.on_secondary_click)

    def on_secondary_click(self, widget, button, time):
        menu = Gtk.Menu()
        submenu = Gtk.Menu()

        menu_item1 = Gtk.MenuItem(label = "First Entry", submenu= submenu)
        menu.append(menu_item1)
        #menu_item1.connect("activate", print, 'll')

        menu_item2 = Gtk.MenuItem(label = "Quit")
        submenu.append(menu_item2)
        menu_item2.connect("activate", Gtk.main_quit)

        submenu.show_all()
        submenu.popup(None, None, None, self, 3, time)
        menu.show_all()
        menu.popup(None, None, None, self, 4, time)

if __name__ == '__main__':
    tray = TrayIcon()

    Gtk.main()

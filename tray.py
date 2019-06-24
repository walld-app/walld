#!/bin/python3
import PySimpleGUIQt as sg
import core

walld = core.Walld()

menu_def = ['BLANK', ['&Open', '---', 'spin_dice', '&Save', 'Category',core.get_categories(),\
'Resolution', ['16:9::res', '16:10::res', '21:9::res'], 'E&xit']]

tray = sg.SystemTray(menu=menu_def, filename=r'temp/kk.x-icon')

def make_flip(item):
    if '*' in item:
        pass
    else:
        if "category_" in item:
            menu_def[1][5][menu_def[1][5].index(item)] = '* ' + item
#            for i in menu[menu.index('Category') + 1]: #+1 необходим для попадания в подкатегории
#                print(i)
#                if i == item:
#                    print (menu,'\n')
#                    print(menu[menu.index('Category') + 1].index(item))
#                    menu[[menu.index('Category')][menu.index('Category')].index(item)] = item + '*' #убейте меня нахуй
def tray_start():
    while True:  # The event loop
        menu_item = tray.Read()
        print(menu_item)
        if menu_item == 'Exit':
            break

        elif menu_item == 'Open':
            sg.Popup('Menu item chosen', menu_item)

        elif menu_item == 'show_popup':
            sg.ShowMessage('LOH')

        elif 'category_' in menu_item:
            make_flip(menu_item)
            tray.Update(menu=menu_def)
        #ТУТ НУЖЕН ЦИКЛ FOR ДЛЯ ПРОШЕРСТЕНИЯ ВСЕХ ЛИСТОВ
            pass
        elif 'res' in menu_item:
            menu_def[1][7][menu_def[1][7].index(menu_item)] = '*' + menu_item
            tray.Update(menu=menu_def)

        elif menu_item == 'spin_dice':
            walld.spin_dice(99)

        elif menu_item == 'Save':
            print(walld.save_image())
tray_start()

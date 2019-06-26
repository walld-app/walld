#!/bin/python3
import PySimpleGUIQt as sg
import core
import sqlworker
import config

walld = core.Walld()
sql = sqlworker.Sql('./temp/tt.db')

menu_def = ['BLANK', ['spin_dice', '---', '&Save', 'Save as...', 'Category',core.get_categories(),\
'Resolution', ['16:9::res_', '16:10::res_', '21:9::res_'], 'E&xit']]

tray = sg.SystemTray(menu=menu_def, filename=r'temp/kk.x-icon')

def make_flip(item):
    print('making flip')
    if "category_" in item:
        target = menu_def[1][5][menu_def[1][5].index(item)]
    elif "res_" in item:
        target = menu_def[1][7][menu_def[1][7].index(item)]
    if '*' in item:
        pass
    else:
        target = '*' + item
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

        elif menu_item == 'Save as...':
            apath = sg.PopupGetFile('hi',save_as=True, file_types=(('PNG files', '*.png' ),('JPEG files', '*.jpg')))
            walld.save_image(apath)

        elif 'category_' in menu_item:
            make_flip(menu_item)
            tray.Update(menu=menu_def)
        #ТУТ НУЖЕН ЦИКЛ FOR ДЛЯ ПРОШЕРСТЕНИЯ ВСЕХ ЛИСТОВ
            pass
        elif 'res' in menu_item:
            make_flip(menu_item)
            tray.Update(menu=menu_def)

        elif menu_item == 'spin_dice':
            walld.spin_dice(99)

        elif menu_item == 'Save':
            walld.save_image()
tray_start()

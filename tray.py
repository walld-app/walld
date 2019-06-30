#!/bin/python3
import PySimpleGUIQt as sg
import core
import config

walld = core.Walld()

menu_def = ['BLANK', ['spin_dice', '---', '&Save', 'Save as...', 'Category',core.get_categories(),\
'Resolution', ['16:9::res_', '16:10::res_', '21:9::res_'], 'E&xit']]

tray = sg.SystemTray(menu=menu_def, filename=r'temp/kk.x-icon')

def make_flip(item):
    if "category_" in item:
        place = 5
    elif "res_" in item:
        place = 7
    if '*' in item:
        menu_def[1][place][menu_def[1][place].index(item)] = item[1:]
        walld.remove_option(item)
    else:
        menu_def[1][place][menu_def[1][place].index(item)] = '*' + item
        walld.add_option(item)
def tray_start():
    #необходимо поставить выделения все сначала выдернув их из базы
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

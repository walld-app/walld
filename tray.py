#!/bin/python3
import PySimpleGUIQt as sg # сука, уже не катит
import core
import config

walld = core.Walld(config.API, config.MAIN_FOLDER)

menu_def = ['BLANK', ['spin_dice', '---', '&Save', 'Save as...', 'Category',walld.get_categories(),\
'Resolution', ['16:9::res_', '16:10::res_', '21:9::res_'], 'E&xit', '!master']]

print(menu_def)
tray = sg.SystemTray(menu=menu_def, filename=r'temp/kk.x-icon')

def make_flip(item): #что если сразу лезть в файл настроек и там все менять? далее вызывать tray_update()
    if "cat_" in item:
        print('cat in item')
        place = 5
    elif "res_" in item:
        place = 7
    elif "sca_" in item:
        place =  6
    if '*' in item:
        menu_def[1][place][menu_def[1][place].index(item)] = item[1:]
        walld.change_option(item[1:])
    else:
        menu_def[1][place][menu_def[1][place].index(item)] = '*' + item
        walld.change_option(item, add=True)
    tray.Update(menu=menu_def)

def restore_settings():
    for i in walld.get_settings()['categories']:
        menu_def[1][5][menu_def[1][5].index(i)] = "*" + i
    for i in walld.get_settings()['resolutions']:
        menu_def[1][7][menu_def[1][7].index(i)] = "*" + i
    tray.Update(menu=menu_def)

def tray_start():
    restore_settings()
    while True:  # The event loop
        menu_item = tray.Read()
        if menu_item == 'Exit':
            break

        elif menu_item == 'Save as...':
            apath = sg.PopupGetFile('hi',save_as=True, file_types=(('PNG files', '*.png' ),('JPEG files', '*.jpg')))
            walld.save_image(apath)

        elif menu_item == '__ACTIVATED__':
            walld.spin_dice()

        elif 'cat_' in menu_item:
            make_flip(menu_item)
            
        #ТУТ НУЖЕН ЦИКЛ FOR ДЛЯ ПРОШЕРСТЕНИЯ ВСЕХ ЛИСТОВ
        elif 'res_' in menu_item:
            make_flip(menu_item)
            
        elif 'sca_' in menu_item:
            make_flip(menu_item)
           
        elif menu_item == 'spin_dice':
            walld.spin_dice()

        elif menu_item == 'Save':
            walld.save_image()

tray_start()

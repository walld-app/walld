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
    #if "cat_" in item:
     #   print('cat in item')
    #    place = 5
    if '*' in item:
        if 'sca_' in item:
            place =  5
            var = item.split('::')[2]+'::cat_'
            second = menu_def[1][place].index(var) +1
            last = (menu_def[1][place][second].index(item))
            menu_def[1][place][second][last] = item[1:]
        elif "res_" in item:
            place = 7
            menu_def[1][place][menu_def[1][place].index(item)] = item[1:]
        #menu_def[1][place][menu_def[1][place].index(item)] = item[1:] #dont touch it dumbass
        walld.change_option(item)
    else:
 # было бы круто поработать тут, необходимо пройтись по всему листу и под листам и раздать/убрать звездочки
        if 'sca_' in item:
            place =  5
            var = item.split('::')[2]+'::cat_'
            second = menu_def[1][place].index(var) +1
            last = (menu_def[1][place][second].index(item))
            menu_def[1][place][second][last] = '*' + item
        elif "res_" in item:
            place = 7
            menu_def[1][place][menu_def[1][place].index(item)] = '*' + item
        walld.change_option(item, add=True)
    tray.Update(menu=menu_def)

def restore_settings():
    for i in walld.get_settings()['categories']:
        for l in walld.get_settings()['categories'][i]:
            nibba = l +'::sca_::' +i
            second = menu_def[1][5].index(i+'::cat_') +1
            last = (menu_def[1][5][second].index(nibba))
            menu_def[1][5][second][last] = "*" + nibba
    for i in walld.get_settings()['resolutions']:
        menu_def[1][7][menu_def[1][7].index(i)] = "*" + i
    tray.Update(menu=menu_def)

def tray_start():
    restore_settings()
    while True:  # The event loop
        menu_item = tray.Read()
        print(menu_item)
        if menu_item == 'Exit':
            break

        elif menu_item == 'Save as...':
            apath = sg.PopupGetFile('hi',save_as=True, file_types=(('PNG files', '*.png' ),('JPEG files', '*.jpg')))
            walld.save_image(apath)

        elif menu_item == '__ACTIVATED__':
            walld.spin_dice('ll')

        elif ('cat_' in menu_item or 'res_' in menu_item or 'sca_' in menu_item) :
            print('aha')
            make_flip(menu_item)
            
        #ТУТ НУЖЕН ЦИКЛ FOR ДЛЯ ПРОШЕРСТЕНИЯ ВСЕХ ЛИСТОВ
           
        elif menu_item == 'spin_dice':
            walld.spin_dice('ll')

        elif menu_item == 'Save':
            walld.save_image()

tray_start()

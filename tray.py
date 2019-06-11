#!/bin/python3
import PySimpleGUIQt as sg
import walld

menu_def = ['BLANK', ['&Open', '---', 'spin_dice', '&Save', 'сосать',['хуй','пезду','кок'],\
'Resolution', ['16:9::res', '16:10::res', '21:9::res'], 'E&xit']]

walld = walld.Walld()

tray = sg.SystemTray(menu=menu_def, filename=r'temp/kk.x-icon')
def tray_start():
    while True:  # The event loop
        menu_item = tray.Read()
        print(menu_item)
        if menu_item == 'Exit':
            break

        elif menu_item == 'Open':
            sg.Popup('Menu item chosen', menu_item)

        elif '*' in menu_item: # ВОПРОС А ЕСЛИ МЫ ПОЛУЧИМ ДРУГУЮ КАТЕГОРИЮ? НУЖНО СДЕЛАТЬ ПОИС ЧУТЬ ГЛОБАЛЬНЕЙ
        #ТУТ НУЖЕН ЦИКЛ FOR ДЛЯ ПРОШЕРСТЕНИЯ ВСЕХ ЛИСТОВ
            print('ok')
            menu_def[1][7][menu_def[1][7].index(menu_item)] = menu_item[1:]
            tray.Update(menu=menu_def)

        elif 'res' in menu_item:
            menu_def[1][7][menu_def[1][7].index(menu_item)] = '*' + menu_item
            tray.Update(menu=menu_def)

        elif menu_item == 'spin_dice':
            walld.spin_dice(95)

        elif menu_item == 'Save':
            print(walld.save_image())
tray_start()

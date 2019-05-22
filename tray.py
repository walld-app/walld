import PySimpleGUIQt as sg

menu_def = ['BLANK', ['&Open', '---', '&Save', 'сосать',['хуй','пезду','кок'], ['1', '2', ['a', 'b']],\
'Resolution', ['1920x1080', '2160x1080'], 'E&xit']]

tray = sg.SystemTray(menu=menu_def, filename=r'kk.x-icon')

while True:  # The event loop
    menu_item = tray.Read()
    print(menu_item)
    if menu_item == 'Exit':
        break
    elif menu_item == 'Open':
        sg.Popup('Menu item chosen', menu_item)
    elif menu_item == '2160x1080':
        menu_item[1][7][1] = 'kok'

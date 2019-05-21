import PySimpleGUIQt as sg

menu_def = ['BLANK', ['show some joke', '&Open', '---', '&Save', ['1', '2', ['a', 'b']], '&Properties', 'E&xit']]

tray = sg.SystemTray(menu=menu_def, filename=r'default_icon.ico')

while True:  # The event loop
    menu_item = tray.Read()
    print(menu_item)
    if menu_item == 'Exit':
        break
    elif menu_item == 'Open':
        sg.Popup('Menu item chosen', menu_item)
    elif menu_item == 'show some joke':
        ShowMessage('hello', 'omg', filename=None, data=None, data_base64=None, messageicon=None, time=10000)

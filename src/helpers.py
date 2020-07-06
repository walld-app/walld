# TODO 500/404 handler
from requests.exceptions import ConnectionError, ConnectTimeout
from requests import get
# from config import log

def api_talk_handler(function):
    def wrapper():
        for i in range(5):
            try:
                function()
                break
            except (ConnectionError, ConnectTimeout):
                print('Something is happening with server, trying again...')
        print('giving up')
        raise ConnectionError

def download(url, file_name):
    '''downloads a file, first comes url, second comes full path of file'''
    with open(file_name, "wb") as file:
        url = url.replace('s', '', 1)
        response = get(url)
        file.write(response.content)
    return file_name

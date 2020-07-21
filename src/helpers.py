# TODO 500/404 handler
import requests
from requests import get
# from config import log

def api_talk_handler(function):
    def wrapper(*args, **kwargs):
        for _ in range(5):
            try:
                final = function(*args, **kwargs)
                return final
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.ConnectTimeout):
                print('Something is happening with server, trying again...')
        print('giving up')
    return wrapper

def download(url, file_name):
    '''downloads a file, first comes url, second comes full path of file'''
    with open(file_name, "wb") as file:
        url = url.replace('s', '', 1)
        response = get(url)
        file.write(response.content)
    return file_name


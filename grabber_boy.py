import sqlite3, requests, json, config


conn = sqlite3.connect('db.db')
cursor = conn.cursor()
print('making new db')
cursor.execute("""CREATE TABLE pics
(id integer, category text, width integer, height integer, url text, file_type text, sub_category text)
""")
conn.commit()

num = 0
for i in range(0, 10000):
    PARAMS = {'auth':config.KEY, "method":"category",'id':'1',
    'page':i, 'width': '1920',
    'height':'1080', 'operator':'min', 'info_level':'2'}
    r = json.loads(requests.get(config.API, params=PARAMS).text)

    print('aha!', num)
    num += 1
    if r['success']:
        if r['wallpapers']:
            for l in r['wallpapers']:
                list = [(l['id'], l['category'], l['width'], l['height'], l['url_image'], l['file_type'], '')]
                cursor.executemany("INSERT INTO pics VALUES (?,?,?,?,?,?,?)",list)
    else:
        print('breaking!')
conn.commit()
conn.close()

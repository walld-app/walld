import sqlite3

class Sql:
    def __init__(self, db_name):
        self.db_name = db_name
        print('sql class is started, checking db!')
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM pics")
            print('found db!')
        except sqlite3.OperationalError:
            print('making new db')
            cursor.execute("""CREATE TABLE pics
            (id integer, category text, sub_category text, url text,
            how_many_used integer, likes integer, extra text)
            """)
            cursor.execute("""CREATE TABLE settings
            (categorys text, resolution text, api text,
            how_many_used integer, likes integer, extra text)
            """)
            cursor.execute("""INSERT INTO settings VALUES
            ('', '', '', '', '', '')""")
            conn.commit()
    def change_option(self, category):
        pass

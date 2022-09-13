import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

"""def select(sql):
    con = sqlite3.connect('./Rotom.db')
    cur = con.cursor()
    cur.execute(sql)
    for row in cur:
        print(row)
    con.close()"""


def insert_users(email, password):
    con = sqlite3.connect('./Rotom.db')
    cur = con.cursor()
    # sql = 'INSERT INTO users2 (email, password) values (?,?)'
    # data = ["kawara@1177", '130']
    try:
        cur.execute("""INSERT INTO users (email, password) values (?,?)""", (email, generate_password_hash(password)))
    except:
        return False
    con.commit()
    con.close()



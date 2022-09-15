import sqlite3


# パスの指定を各自お願いします
dbname = ".\Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute(
    """DROP TABLE ???;"""
)

conn.close()
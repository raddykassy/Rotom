# table作成時に1度だけ実行
import sqlite3

# Rotom.dbに接続
dbname = ".\Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()
# SQLを実行
cur.execute(
    """CREATE TABLE bb
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     email TEXT, password TEXT, 
     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""
)

conn.close()
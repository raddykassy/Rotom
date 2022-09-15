# table作成時に1度だけ実行
import sqlite3

# Rotom.dbに接続
dbname = ".\Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()
# SQLを実行

"""usersテーブル
・id 主キー
・email 
・password ハッシュ化して格納
・name ユーザネーム
・date 登録日
"""
cur.execute(
    """CREATE TABLE users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     email TEXT NOT NULL, 
     password TEXT NOT NULL, 
     name TEXT, 
     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""
)

conn.close()
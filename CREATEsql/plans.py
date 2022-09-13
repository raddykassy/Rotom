# table作成時に1度だけ実行
# plansテーブルの作成
import sqlite3

dbname = ".\Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute(
    """CREATE TABLE plans(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    schedule TEXT,
    url TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id));"""
)

conn.close()
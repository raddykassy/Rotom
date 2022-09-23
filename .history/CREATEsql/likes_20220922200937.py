# coding:utf-8
# テーブル作成時に1度だけ実行
# plan_placesの作成
import sqlite3

dbname = "../Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

"""likesテーブル
・id:主キー
・plan_id:外部キー(planテーブルid格納)
・user_id:外部キー(userテーブルid格納)
・created_at:いいねしたときのtimestamp
"""

cur.execute(
    """CREATE TABLE likes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TEXT,
    FOREIGN KEY(plan_id) REFERENCES plans(id),
    FOREIGN KEY(user_id) REFERENCES users(id));"""
)

conn.close()

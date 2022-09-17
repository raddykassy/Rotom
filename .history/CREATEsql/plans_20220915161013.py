# coding:utf-8
# table作成時に1度だけ実行
# plansテーブルの作成
import sqlite3

dbname = ".\Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

"""
plansテーブル
・id 主キー
・user_id usersテーブルの外部キー
・title プランのタイトル
・description プランの説明　null許容
・schedule スケジュールを格納 null許容
・url 動画のurlを格納 null許容
・date 登録日
"""

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

INSERT INTO plans(user_id, title, url) VALUES (1, "長野新幹線旅行旅", "https://youtu.be/kQpssznrf-g");

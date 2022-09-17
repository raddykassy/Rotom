# coding:utf-8
# テーブル作成時に1度だけ実行
# plan_placesの作成
import sqlite3

dbname = ".\Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

"""plan_placesテーブル
・id 主キー
・plan_id 外部キー（planテーブルid格納）
・place 場所の名前
・description 説明
・latitude 緯度
・longitude 経度
"""

cur.execute(
    """CREATE TABLE plan_places(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    place TEXT NOT NULL,
    description TEXT,
    latitude REAL,
    longitude REAL,
    FOREIGN KEY(plan_id) REFERENCES plans(id));"""
)

conn.close()
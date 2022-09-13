# テーブル作成時に1度だけ実行
# plan_placesの作成
import sqlite3

dbname = ".\Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute(
    """CREATE TABLE plan_places(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    place TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY(plan_id) REFERENCES plans(id));"""
)

conn.close()
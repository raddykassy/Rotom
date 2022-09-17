# coding:utf-8

import sqlite3

dbname = "./Rotom.db"
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute(
    """DROP TABLE ???;"""
)

conn.close()
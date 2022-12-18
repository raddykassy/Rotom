# psycopg2 モジュールのインポート
import psycopg2
import settings

pas = settings.PASS

# PostgreSQL Server へ接続
# 開発用
# conn =  psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
#                 user="postgres",        #ユーザ
#                 password=pas,  #パスワード
#                 host="localhost",       #ホスト名
#                 port="5432",            #ポート
#                 dbname="postgres"))    #データベース名

# render用
conn =  psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
                user="rotom_qtnb_user",        #ユーザ
                password=pas,  #パスワード
                host="dpg-cefa7r1gp3jk7mh3d7qg-a",       #ホスト名
                port="5432",            #ポート
                dbname="rotom_qtnb"))    #データベース名


# conn = psycopg2.connect('host=localhost port=5432 dbname=postgres user=postgres password={}', format(pas))
cur = conn.cursor()

sql1 = """
        CREATE TABLE plans (
            id serial PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            title TEXT NOT NULL,
            description TEXT,
            url TEXT,
            posted_at TIMESTAMP,
            days TEXT,
            costs TEXT
        );
     """

sql2 = """
        DROP TABLE users;"""


# テーブルを作る
cur.execute(sql1)


# コミットし、変更を確定する
conn.commit()

# 接続を閉じる
conn.close()
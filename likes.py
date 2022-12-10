# psycopg2 モジュールのインポート
import psycopg2
import settings

pas = settings.PASS

# PostgreSQL Server へ接続
conn =  psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
                user="postgres",        #ユーザ
                password=pas,  #パスワード
                host="localhost",       #ホスト名
                port="5432",            #ポート
                dbname="postgres"))    #データベース名


# conn = psycopg2.connect('host=localhost port=5432 dbname=postgres user=postgres password={}', format(pas))
cur = conn.cursor()

sql1 = """
        CREATE TABLE likes (
            id serial PRIMARY KEY,
            plan_id INTEGER NOT NULL REFERENCES plans(id),
            user_id INTEGER NOT NULL REFERENCES users(id),
            created_at TIMESTAMP
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
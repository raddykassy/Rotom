from turtle import title
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required
import secrets
import requests
import json
# import flask_paginate
from flask_paginate import Pagination, get_page_parameter
import datetime




app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ログインしているかどうか判別するグローバル変数
# False = logout状態, True = login状態
status = False

# -------------------------------------------------------------------
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
# ---------------------------------------------------------------------

@app.route('/')
def index():
    # グローバル変数を宣言
    global status

    # statusがTrue(login状態)ならusersテーブルからemailを取得
    # index2.htmlにemailを渡して、表示する
    if status == True:
        user_id = session["id"]
        con = sqlite3.connect('Rotom.db')
        cur = con.cursor()
        # ここnameにしてもいいかも
        cur.execute("SELECT email FROM users WHERE id = ?", (user_id,))
        user_info =  cur.fetchall()
        con.close()

        return render_template('index2.html', status=status, email=user_info[0][0])

    else:
        return render_template('index2.html', status=status)


# loginページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: loginページの表示
    POST: username, passwordの取得, sesion情報の登録
    """
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get('password')
        # hash = generate_password_hash(password)
        global status

        error_message = ""

        con = sqlite3.connect('Rotom.db')
        cur = con.cursor()
        # SELECT * より修正 9/20 passwordのみからpassword, idに変更
        cur.execute("SELECT password, id FROM users WHERE email = ?", (email,))
        user_data = cur.fetchall()

        # メールアドレス：ユーザーデータは1:1でないといけない（新規登録画面でその処理書いてくれると嬉しいです！（既に同じメールアドレスが存在している場合はエラーメッセージを渡す等））
        if len(user_data) == 1:
            for row in user_data:
                if check_password_hash(row[0], password):
                    con.close()
                    session["id"] = row[1]
                    status = True
                    return redirect("/")
                    # return render_template("index2.html", status=status)
                else:
                    con.close()
                    error_message = "パスワードが異なります"
                    return render_template("login.html", error_message=error_message)
        else:
            con.close()
            # ↓現段階では登録されていない or メールアドレスが重複して登録されている
            error_message = "入力されたメールアドレスは登録されていません"
            return render_template("login.html", error_message=error_message)

        # """
        # <h1>ログインに成功しました</h1>
        # <p><a href='/'> ⇒top page</p>
        # """

    else:
        return render_template("login.html")


# logout
@app.route("/logout")
# @login_required
def logout():
    # セッション情報をクリア
    session.clear()
    # グローバル変数をlogout状態に
    global status
    status = False
    return """
           <h1>ログアウトしました</h1>
           <p><a href="/"> ⇒top page</p>
    """

# register
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET: register.htmlの表示
    POST: ユーザの追加
    """

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get('password')
        confirmation = request.form.get('confirm-password')
        username = request.form.get('user-name')

        error_message = ""

        if password != confirmation:
            error_message = "確認用パスワードと一致しませんでした。"
            # エラーメッセージ付きでregister.htmlに渡す
            return render_template("register.html", error_message=error_message)

        con = sqlite3.connect('Rotom.db')
        cur = con.cursor()
        cur.execute("SELECT email FROM users")
        email_data = cur.fetchall()

        # emailが登録済みか確認する
        for row in email_data:
            if row[0] == email:
                con.close
                error_message = "そのemailアドレスは登録済みです"
                # エラーメッセージ付きでregister.htmlに渡す
                return render_template("register.html", error_message=error_message)
        # ユーザ情報をusersテーブルに登録
        cur.execute("""INSERT INTO users (email, password, name) values (?,?,?)""", (email, generate_password_hash(password), username,))
        con.commit()
        con.close()
        # 新規登録後はlogin画面へ
        return redirect ("/login")

    else:
        return render_template("register.html")

@app.route("/post", methods=["GET", "POST"])
def post():
    """
    GET: post.htmlの表示
    POST: planの追加
    """
    if request.method == 'POST':

        user = session["id"]
        # plansテーブル
        plan_title = request.form.get("plan-title")
        plan_description = request.form.get("description")
        url = request.form.get("vlog-url")
        place_sum = request.form.get("place_sum")

        # place_names と place_idに情報を追加していく
        place_names = []
        place_id = []

        # place_sum分place_nameとplace_idを取得し、リストに入れる
        for i in range(int(place_sum)):
            name = ("place_name_%s" %str(i+1))
            id = ("place_id_%s" %str(i+1))
            # print(tmp str(i))
            # t = request.form.get(tmp, i)

            tmp_name = request.form.get(name)
            tmp_id = request.form.get(id)

            place_names.append(tmp_name)
            place_id.append(tmp_id)
        """
        print("-----------")
        print(place_names)
        print(place_id)
        print("-----------")
        """
        # リストからNoneを削除する
        place_names = list(filter(None, place_names))
        place_id = list(filter(None, place_id))


        # plansテーブルにinsert
        con = sqlite3.connect('Rotom.db')
        cur = con.cursor()
        cur.execute("""SELECT id FROM users WHERE id = ?""", (user,) )

        for row in cur.fetchall():
            user_id = row
        cur.execute("""INSERT INTO plans (user_id, title, description, url) VALUES (?,?,?,?)""", (user_id[0], plan_title, plan_description, url))
        con.commit()
        con.close()

        # plan_detailテーブルにinsert
        con = sqlite3.connect('Rotom.db')
        cur = con.cursor()
        cur.execute("""SELECT id FROM plans WHERE title = ?""", (plan_title,))
        for row in cur.fetchall():
            plan_id = row

        for n  in range(len(place_names)):
            cur.execute("INSERT INTO plan_places(plan_id, place_id, place_name, number) VALUES(?,?,?,?)", (plan_id[0], place_id[n], place_names[n], n+1))

        # for i in range():

        con.commit()
        con.close()

        return redirect("/")

    else:
        return render_template("post.html")


@app.route('/inquiry')
def inquiry():
    return render_template('inquiry.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/serach')
def search():
    return render_template('search.html')

@app.route('/content')
def content():
    return render_template('content.html')

#データベースから取ってきた値を辞書形式で扱えるように
def user_lit_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/plans')
def plans():
    #データベースから情報を取ってきて、plans.htmlに渡す。
    #渡す情報　plan_places, plans
    dbname = "Rotom.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = user_lit_factory

    cur = conn.cursor()

    #plansを全て取得
    plans = list(cur.execute("SELECT * FROM plans"))

        #urlからyoutubeIDを取得
    for index, plan in enumerate(plans):
        plan["video_id"] = plan["url"].split("/")[3]

    #ここからページネーション機能
    
    # (1) 表示されているページ番号を取得(初期ページ1)
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # (2)１ページに表示させたいデータ件数を指定して分割(１ページに3件表示)
    PageData = plans[(page - 1)*6: page*6]

    # (3) 表示するデータリストの最大件数から最大ページ数を算出
    MaxPage = (- len(plans) // 6) * -1
    
    print(len(plans))
    print(MaxPage)
    
    return render_template('plans.html',plans=PageData, CurPage=page, MaxPage=MaxPage)


#下二行のパラメーターのuser_idは、動画を投稿した人のuser_id
@app.route('/plan_content/<user_id>/<int:post_id>')
def plan_content(user_id, post_id):
    #データベースから情報を取ってきて、content.htmlに渡す。

    dbname = "Rotom.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = user_lit_factory

    cur = conn.cursor()

    place_info_li = list(cur.execute("SELECT * FROM plan_places WHERE plan_id = ?", (post_id,)))
    plan_info = list(cur.execute("SELECT * FROM plans WHERE id=?", (post_id,)))
    like_info = list(cur.execute("SELECT * FROM likes WHERE plan_id = ? AND user_id = ?", (post_id, session["id"],)))


    #place_idから緯度経度を取得
    #place_info_liにlat, lngをappend
    # place_info_li = [{}, {}, ...]
    for index, place_info in enumerate(place_info_li):
        #place_idから情報を取得
        response = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_info["place_id"]}&key=AIzaSyDSB9wJUooZ1GlQFPqjUUBZmFLp7Y04HzI').json()
        place_info_li[index]["url"] = response["result"]["website"]
        place_info_li[index]["lat"] = response["result"]["geometry"]["location"]["lat"]
        place_info_li[index]["lng"] = response["result"]["geometry"]["location"]["lng"]

    return render_template('content.html', plan_info = plan_info, user_id = user_id, place_info_li = place_info_li)

@app.route('/like', methods=['GET', 'POST'])
def like():
    
    if request.method=="POST":

        dt_now = datetime.datetime.now()

        plan_id = request.json['plan_id']
        user_id = session["id"]

        #データベースから情報を取ってくる
        dbname = "Rotom.db"
        conn = sqlite3.connect(dbname)
        conn.row_factory = user_lit_factory
        cur = conn.cursor()

        like_info = list(cur.execute("SELECT * FROM likes WHERE plan_id = ? AND user_id = ?", (plan_id, user_id,)))

        #過去にLikeしたことがない場合、新たに列を追加
        if like_info == []:
            cur.execute("INSERT INTO likes (plan_id, user_id, created_at) VALUES (?, ?, ?)", (plan_id, user_id, dt_now,))
            like_info = list(cur.execute("SELECT * FROM likes WHERE plan_id = ? AND user_id = ?", (plan_id, user_id,)))
            conn.commit()
            conn.close()

        #過去にLikeしたことがある場合、データベースから削除
        else:
            cur.execute("DELETE FROM likes WHERE plan_id = ? AND user_id = ?", (plan_id, user_id,))
            # like_info = list(cur.execute("SELECT * FROM likes WHERE plan_id = ? AND user_id = ?", (plan_id, user_id)))
            conn.commit()
            conn.close()



    return redirect("/")

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')

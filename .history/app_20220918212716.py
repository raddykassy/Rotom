from turtle import title
from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash
from helpers import login_required
import secrets
import requests
import json


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# -------------------------------------------------------------------
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
# ---------------------------------------------------------------------

@app.route('/')
def index():
    # print(USERLIST)
    return render_template('index.html')


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
        hash = generate_password_hash(password)

        con = sqlite3.connect('Rotom.db')
        cur = con.cursor()
        cur.execute("SELECT* FROM users WHERE email = ?", (email,))
        for row in cur.fetchall():
            if row == hash:
                break
        con.commit()
        con.close()        


        session["email"] = email

        return """
        <h1>ログインに成功しました</h1>
        <p><a href='/'> ⇒top page</p>
        """

    else:
        return render_template("login.html")


# logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
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

        if password != confirmation:
            return """<h1>passwordが一致しません</h1>"""
        
        con = sqlite3.connect('Rotom.db')
        cur = con.cursor()
        try:
            cur.execute("""INSERT INTO users (email, password) values (?,?)""", (email, generate_password_hash(password)))
        except:
            return False
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

        user = session["email"]
        # plansテーブル
        plan_title = request.form.get("plan-title")
        plan_description = request.form.get("description")
        # schedule = request.form.get("schedule")
        url = request.form.get("vlog-url")

        # plan_placesテーブル
        # place01 = request.form.get("place01")
        place_names = []
        place_id = []

        for i in range(5):
            name = ("place_name_%s" %str(i+1))
            id = ("place_id_%s" %str(i+1))
            # print(tmp str(i))
            # t = request.form.get(tmp, i)

            tmp_name = request.form.get(name)
            tmp_id = request.form.get(id)

            place_names.append(tmp_name)
            place_id.append(tmp_id)
        
        print("-----------")
        print(place_names)
        print(place_id)
        print("-----------")

        place_names = list(filter(None, place_names))
        place_id = list(filter(None, place_id))

        """
        for i in places:
            if (" ") in places[i]:
                places[i].split()
                print("------------")
                print(places[i][0])
                print(places[i][1])
                print("-------------")
        """

        # plansテーブルにinsert
        con = sqlite3.connect('Rotom.db')
        cur = con.cursor()
        cur.execute("""SELECT id FROM users WHERE email = ?""", (user,) )
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
    return render_template('plans.html',plans=plans)


@app.route('/plan_content/<user_id>/<int:post_id>')
def plan_content(user_id, post_id):
    #データベースから情報を取ってきて、content.htmlに渡す。

    dbname = "Rotom.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = user_lit_factory

    cur = conn.cursor()

    place_info_li = list(cur.execute("SELECT * FROM plan_places WHERE plan_id = ?", (post_id,)))
    plan_info = list(cur.execute("SELECT * FROM plans WHERE id=?", (post_id,)))

    #place_idから緯度経度を取得
    #place_info_liにlat, lngをappend
    for place_info in place_info_li:
        response = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_info["place_id"]}&key=AIzaSyDSB9wJUooZ1GlQFPqjUUBZmFLp7Y04HzI')
        print(place_info)
        print(response.json)
    

    return render_template('content.html', plan_info = plan_info, username = user_id, place_info_li = place_info_li)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')

from turtle import title
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "123456789rotom"

USERLIST = {
    'kaito@gmail.com':'114',
    'ryoga@gmail.com':'066',
    'kosuke@gmail.com':'112',
    'h.kawara1717@gmail.com':'126'
}

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

        if not email in USERLIST:
            return """<h1>email または password が間違っています</h1>"""
        if USERLIST[email] != password:
            return """<h1>email または password が間違っています</h1>"""
        
        session[email] = email

        return """
        <h1>ログインに成功しました</h1>
        <p><a href='/'> ⇒top page</p>
        """

    else:
        return render_template("login.html")


# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

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

        if email in USERLIST:
            return """<h1>このemailは登録済みです<h1>"""
        if password != confirmation:
            return """<h1>passwordが一致しません</h1>"""

        # 辞書に追加(flask終了するごとにUSERLISTはリセット)
        USERLIST[email]=password
        # print(USERLIST)
        return redirect ("/")


    else:
        return render_template("register.html")

@app.route("/post", methods=["GET", "POST"])
def post():
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


@app.route('/plan_content/<username>/<int:post_id>')
def plan_content(username, post_id):
    #データベースから情報を取ってきて、content.htmlに渡す。

    dbname = "Rotom.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = user_lit_factory

    cur = conn.cursor()

    place_info_li = list(cur.execute("SELECT * FROM plan_places WHERE plan_id = ?", (post_id,)))
    plan_info = list(cur.execute("SELECT * FROM plans WHERE id=?", (post_id,)))

    print()
    return render_template('content.html', plan_info = plan_info, username = username, place_info_li = place_info_li)


from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from sql import insert_users
from helpers import login_required
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


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

        con = sqlite3.connect('.\Rotom.db')
        cur = con.cursor()
        cur.execute("SELECT* FROM users WHERE email = ?", (email,))
        for row in cur.fetchall():
            if row == hash:
                break

        # print("---------")
        # print(len(cur.fetchall()))
        # l = len(cur.fetchall())
        # print(l)
        # if len(cur.fetchall()) != "1":
            # return """<h1>入力に誤りがあります</h1>"""
        #if (cur.fetchall[0][2]) !=  hash:
            #return """<h1>どんまい</h1>"""
        con.commit()
        con.close()        

        # セッションにemailを格納、login処理
        # print("success")      
        session[email] = email

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

        if password != confirmation:
            return """<h1>passwordが一致しません</h1>"""
        con = sqlite3.connect('.\Rotom.db')
        cur = con.cursor()
        try:
            cur.execute("""INSERT INTO users (email, password) values (?,?)""", (email, generate_password_hash(password)))
        except:
            return False
        con.commit()
        con.close()

<<<<<<< HEAD
        # 新規登録後はlogin画面へ
        return redirect ("/login")
=======
        # 辞書に追加(flask終了するごとにUSERLISTはリセット)
        USERLIST[email]=password
        # print(USERLIST)
        return redirect ("/")
>>>>>>> cea3e8429f4d1c7d5671a46eea32c287e07ffedc


    else:
        return render_template("register.html")

<<<<<<< HEAD
@app.route('/post')
@login_required
def post():
    return render_template('post.html')
=======
@app.route("/post", methods=["GET", "POST"])
def post():
    return render_template("post.html")
>>>>>>> cea3e8429f4d1c7d5671a46eea32c287e07ffedc

@app.route('/inquiry')
def inquiry():
    return render_template('inquiry.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/serach')
def search():
    return render_template('search.html')

<<<<<<< HEAD
=======
@app.route('/content')
def content():
    return render_template('content.html')
>>>>>>> cea3e8429f4d1c7d5671a46eea32c287e07ffedc

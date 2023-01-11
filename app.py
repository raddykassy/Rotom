from itertools import count
from turtle import title
from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required
import secrets
import requests
import json
from flask_paginate import Pagination, get_page_parameter
import datetime
import settings
import psycopg2
import psycopg2.extras


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
map_api_key = settings.AP
pas = settings.PASS

# ログインしているかどうか判別するグローバル変数
# False = logout状態, True = login状態
status = False

# -------------------------------------------------------------------
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
# ---------------------------------------------------------------------

#絵文字に対応する16進数を格納したリスト
emoji_array = {
    "airport": "🛩",
    "amusement_park":"🎠",
    "aquarium": "🐠",
    "art_gallery": "🖼",
    "bakery": "🥯",
    "bank":"🏦",
    "bar": "🍺",
    "beauty_salon": "💇‍♀️",
    "bicycle_store":"🚲",
    "book_store":"📚",
    "car_dealer": "🚗",
    "car_rental": "🚗",
    "cafe":"☕",
    "campground":"🏕️",
    "casino": "🎰",
    "city_hall":"🏛",
    "church":"⛪",
    "clothing_store":"👚",
    "convenience_store":"🏪",
    "department_store":"🛍",
    "electronics_store": "🤖",
    "embassy": "🛂",
    "florist":"💐",
    "food":"🍽️",
    "furniture_store": "🛋",
    "gym":"🏋️",
    "hardware_store": "💻",
    "hair_care":"💇‍♀️",
    "hindu_temple":"🛕",
    "home_goods_store":"🛋",
    "jewelry_store":"💎",
    "landmark": "🗽",
    "library":"📚",
    "light_rail_station": "🚉",
    "liquor_store": "🥃",
    "meal_delivery": "😋",
    "meal_takeaway": "😋",
    "mosque": "🕌",
    "movie_theater": "🍿",
    "museum":"🖼️",
    "natural_feature": "🏞",
    "night_club":"💃🏻",
    "parking":"🚗",
    "park":"🏞",
    "place_of_worship": "⛩",
    "rv_park": "🚗",
    "real_estate_agency":"🏢",
    "restaurant":"🍽️",
    "school": "🏫",
    "secondary_school": "🏫",
    "shoe_store":"👟",
    "shopping_mall":"🛍",
    "spa":"💆",
    "stadium":"🏟",
    "store":"🛒",
    "subway_station":"🚇",
    "supermarket":"🛒",
    "synagogue": "🕍",
    "tourist_attraction":"📸",
    "train_station":"🚉",
    "travel_agency": "🧳",
    "transit_station": "🚉",
    "university":"🏫",
    "zoo":"🐘",
    "lodging":"🏨",
}

# postgresのクエリを辞書形式で返すためのfunction
# 引数にクエリを渡す
def get_dict_resultset(sql, *args):
    conn = psycopg2_connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute (sql, (args))
    results = cur.fetchall()
    dict_result = []
    for row in results:
        dict_result.append(dict(row))
    return dict_result

# 開発用
#def psycopg2_connect():
#    conn = psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
#                user="postgres",        #ユーザ
#                password=pas,  #パスワード
#                host="localhost",       #ホスト名
#                port="5432",            #ポート
#                dbname="postgres"))    #データベース名
#    return conn

# デプロイ用
def psycopg2_connect():
    conn = psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
               user="rotom_qtnb_user",        #ユーザ
                password=pas,  #パスワード
                host="dpg-cefa7r1gp3jk7mh3d7qg-a",       #ホスト名
                port="5432",            #ポート
                dbname="rotom_qtnb"))    #データベース名
    return conn

@app.route('/')
def index():

    # グローバル変数を宣言
    global status

    # statusがTrue(login状態)ならusersテーブルからemailを取得
    # index2.htmlにemailを渡して、表示する
    if status:
        user_id = session["id"]
        # PostgreSQL Server へ接続
        con =  psycopg2_connect()
        cur = con.cursor()
        cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        user_info =  cur.fetchall()
        con.close()
        
        # いいねが高いものを取得
        sql = ("""
            SELECT * FROM plans WHERE plans.id IN
            (SELECT DISTINCT plan_id FROM plans INNER JOIN likes ON
            plans.id = likes.plan_id WHERE plans.id IN
            (SELECT plan_id FROM likes GROUP BY plan_id ORDER BY COUNT(plan_id) DESC LIMIT 3)
            LIMIT 3)
        """,)
        # 引数*sqlだとpsycopg2.ProgrammingError: can't execute an empty queryになった
        plans = get_dict_resultset(*sql)

        for index, plan in enumerate(plans):
                plan["video_id"] = plan["url"].split("/")[3]

        session["user_name"] = user_info[0][0]
        return render_template('index2.html', status=status, user_name=session["user_name"], user_id=user_id, plans=plans, map_api_key = map_api_key)

    else:        
        # いいねが高いものを取得
        sql = ("""
            SELECT * FROM plans WHERE plans.id IN
            (SELECT DISTINCT plan_id FROM plans INNER JOIN likes ON
            plans.id = likes.plan_id WHERE plans.id IN
            (SELECT plan_id FROM likes GROUP BY plan_id ORDER BY COUNT(plan_id) DESC LIMIT 3)
            LIMIT 3)
        """,)
        # 引数*sqlだとpsycopg2.ProgrammingError: can't execute an empty queryになった
        plans = get_dict_resultset(*sql)

        for index, plan in enumerate(plans):
                plan["video_id"] = plan["url"].split("/")[3]

        return render_template('index2.html', status=status, plans=plans,  map_api_key = map_api_key)


# loginページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: loginページの表示
    POST: username, passwordの取得, sesion情報の登録
    """
    global status
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get('password')
        # hash = generate_password_hash(password)
        # global status

        error_message = ""

        # PostgreSQL Server へ接続
        con = psycopg2_connect()
        cur = con.cursor()
        cur.execute("SELECT password, id FROM users WHERE email = %s", (email,))
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
    else:
        return render_template("login.html")


# logout
@app.route("/logout")
@login_required
def logout():
    # セッション情報をクリア
    session.clear()
    # グローバル変数をlogout状態に
    global status
    status = False
    flash("ログアウトが完了しました。")
    return redirect("/")

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
        confirmation = request.form.get('confirm_password')
        username = request.form.get('username')

        error_message = ""

        if password != confirmation:
            error_message = "確認用パスワードと一致しませんでした。"
            # エラーメッセージ付きでregister.htmlに渡す
            return render_template("register.html", error_message=error_message)
        # --------------------------------------------------------------------------------
        conn = psycopg2_connect()    #データベース名
        dt = datetime.datetime.now()
        with conn:
            with conn.cursor() as cur:
                
                cur.execute('SELECT * FROM users;')
                # print(cur.fetchall())
                email_data = cur.fetchall()

                for row in email_data:
                    print(row)
                    if row[1] == email:
                        error_message = "そのemailアドレスは登録済みです"
                        # エラーメッセージ付きでregister.htmlに渡す
                        return render_template("register.html", error_message=error_message)

                cur.execute("INSERT INTO users(email, password, name, registered_at) VALUES(%s, %s, %s, %s);", (email, generate_password_hash(password), username, dt))
            conn.commit
        # ------------------------------------------------------------------------

        # 新規登録後はlogin画面へ
        return redirect ("/login")

    else:
        return render_template("register.html")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """
    GET: post.htmlの表示
    POST: planの追加
    """
    global status
    if request.method == 'POST':

        user = session["id"]
        # plansテーブル
        plan_title = request.form.get("plan_title")
        plan_description = request.form.get("description")
        url = request.form.get("vlog_url")
        costs = request.form.get("costs")
        days = request.form.get("days")

        #プランに追加した場所の合計
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

        # リストからNoneを削除する(なくてもいいかも)
        place_names = list(filter(None, place_names))
        place_id = list(filter(None, place_id))

        #セッション情報に登録
        session["place_names"] = place_names
        session["place_id"] = place_id
        session["place_sum"] = place_sum
        session["plan_title"] = plan_title
        session["plan_description"] = plan_description
        session["url"] = url
        session["place_names"] = place_names
        session["place_id"] = place_id
        session["days"] = days
        session["costs"] = costs

        return redirect("/post-details")

    else:
        return render_template("post.html", status=status, user_name=session["user_name"],  map_api_key = map_api_key, user_id=session["id"])

@app.route("/post-details", methods=["GET", "POST"])
@login_required
# 場所別のレビューや予約URLのリンク貼り付けなど、詳細情報記入のページ
def post_details():

    # プラン投稿ボタンが押された時
    if request.method == 'POST':
        data = request.get_json(force=True)
        place_description = data["comment_li"] #場所ごとのコメント
        place_review = data["rating_li"] #場所ごとのレーティング
        booking_url = data["url_li"] #場所ごとの予約URL
        price = data["price_li"] #場所ごとの価格

        # plansテーブルに格納する情報
        user_id = session["id"]
        title = session["plan_title"]
        description = session["plan_description"]
        url = session["url"]
        days = session["days"]
        costs = session["costs"]

        # plansテーブルにinsert
        con =  psycopg2_connect()    #データベース名

        dt = datetime.datetime.now()
        with con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO plans (user_id, title, description, url, posted_at, days, costs) VALUES (%s,%s,%s,%s,%s,%s,%s)", (user_id, title, description, url, dt, days, costs,))
            con.commit

        # plan_placesに格納する情報
        plan_id = "" #データベースからとってくる
        place_id = session["place_id"] #for文で回して取得
        place_names = session["place_names"] #for文で回して取得


        # plan_detailテーブルにinsert

        #plan_idを取ってくる
        with con:
            with con.cursor() as cur:
                cur.execute("SELECT id FROM plans WHERE title = %s ", (title,))
        
                for row in cur.fetchall():
                    plan_id = row


        #場所ごとにplan_placesに格納
        with con:
            with con.cursor() as cur:
                for n  in range(len(session["place_names"])):
                    cur.execute("INSERT INTO plan_places(plan_id, place_id, place_name, number, description, place_review, booking_url, price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (plan_id[0], place_id[n], place_names[n], n+1, place_description[n], place_review[n], booking_url[n], price[n],))
            con.commit()
        flash("投稿が完了しました。")
        return "post_details()での処理が完了"

    else:

        #post.htmlから引き継いだ値を表示
        plan_info = [{"user_id": session["id"], "title": session["plan_title"],  "description":	session["plan_description"], "url": session["url"]}]
        place_info_li = []

        for n  in range(len(session["place_names"])):
            place_info_li.append({"place_name": session["place_names"][n]})

        return render_template('post-details.html', plan_info = plan_info, place_info_li = place_info_li, map_api_key = map_api_key, user_id=session["id"], status=status, user_name=session["user_name"])

@app.route('/inquiry')
def inquiry():
    return render_template('inquiry.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

#データベースから取ってきた値を辞書形式で扱えるように
def user_lit_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/search', methods=["GET", "POST"])
def search():
    global status
    if request.method == 'POST':

        url = request.form.get("vlog_url")
        place = request.form.get("place")
        place_id = request.form.get("place_id_box")

        # 同時に複数項目が入力されている場合
        if url and place:
            error_message = "複数欄を同時に入力することはできません。"
            return render_template('plans.html', error_message=error_message, CurPage=1, MaxPage=1)
        if not url and not place:
            error_message = "いずれかの項目を入力してください。"
            return render_template('plans.html', error_message=error_message, CurPage=1, MaxPage=1)
        # VlogのURLから検索
        elif url:

            sql = ("""
                    SELECT plans.id, plans.user_id, plans.title, plans.description, plans.url, plans.posted_at, plans.costs, plans.days, users.name
                    FROM plans INNER JOIN users ON plans.user_id = users.id WHERE plans.url = %s
                    """, (url,))

            plans = get_dict_resultset(*sql)
            
            if not plans:
                error_message = url + "に関するプランは存在しません"
                return render_template('plans.html', error_message=error_message, CurPage=1, MaxPage=1)

            for index, plan in enumerate(plans):
                plan["video_id"] = plan["url"].split("/")[3]

            #ページネーション機能
            page_info = paginate(plans)

            if status:
                return render_template('plans.html', plans=page_info["plans"], CurPage=page_info["CurPage"], MaxPage=page_info["MaxPage"], status=status, user_name=session["user_name"])
            else:
                return render_template('plans.html', plans=page_info["plans"], CurPage=page_info["CurPage"], MaxPage=page_info["MaxPage"])

        # 場所から検索
        elif place:

            # 入力された場所が含まれるプランを取得
            sql = ("""
                    SELECT DISTINCT plans.id, plans.user_id, plans.title, plans.description, plans.url, plans.posted_at, plans.costs, plans.days, users.name
                    FROM plans INNER JOIN users ON plans.user_id = users.id
                    JOIN plan_places ON plans.id = plan_places.plan_id WHERE place_id = %s
                    """, (place_id,))

            plans = get_dict_resultset(*sql)

            if not plans:
                error_message = place + "を含んだプランは存在しません"
                return render_template('plans.html', error_message=error_message, CurPage=1, MaxPage=1)

            for index, plan in enumerate(plans):
                plan["video_id"] = plan["url"].split("/")[3]

            #ここからページネーション機能

            #ページネーション機能
            page_info = paginate(plans)

            if status:
                return render_template('plans.html', plans=page_info["plans"], CurPage=page_info["CurPage"], MaxPage=page_info["MaxPage"], status=status, user_name=session["user_name"])
            else:
                return render_template('plans.html', plans=page_info["plans"], CurPage=page_info["CurPage"], MaxPage=page_info["MaxPage"])

    # GET methods
    else:
        if status:
            return render_template('search.html', status=status, user_name=session["user_name"])
        else:
            return render_template("search.html")

@app.route('/content')
def content():
    return render_template('content.html',  map_api_key = map_api_key)


@app.route('/plans')
def plans():
    global status
    # plan一覧表示

    # plan取得
    sql = ("""
           SELECT plans.id, plans.user_id, plans.title, plans.description, plans.url,
           plans.posted_at, plans.costs, plans.days, users.name FROM plans
           INNER JOIN users ON plans.user_id = users.id
           """,)

    plans = get_dict_resultset(*sql)
    
    # likes取得
    sql = ("""
            SELECT plan_id
            FROM likes;
            """,)
    
    likes = get_dict_resultset(*sql)

    # like数カウント
    plan_id_num=[]
    planid_like_dic = {}

    for like in likes:
        plan_id_num.append(like["plan_id"])
    else:
        for plan_id in plan_id_num:
            planid_like_dic[plan_id] = int(plan_id_num.count(plan_id))

    # like数をplansに加える
    for plan_index, plan in enumerate(plans):
        if plan["id"] in planid_like_dic.keys():
            plans[plan_index]["likes"] = planid_like_dic[plan["id"]]

    plans.reverse()

    #urlからyoutubeIDを取得
    for index, plan in enumerate(plans):
        plan["video_id"] = plan["url"].split("/")[3]

    #ページネーション機能
    page_info = paginate(plans)

    if status:
        return render_template('plans.html', plans=page_info["plans"], CurPage=page_info["CurPage"], MaxPage=page_info["MaxPage"], status=status, user_name=session["user_name"], user_id=session["id"],  map_api_key = map_api_key)

    else:
        return render_template('plans.html', plans=page_info["plans"], CurPage=page_info["CurPage"], MaxPage=page_info["MaxPage"], status=status,  map_api_key = map_api_key)

#下二行のパラメーターのuser_idは、動画を投稿した人のuser_id
@app.route('/plan_content/<user_id>/<int:post_id>')
def plan_content(user_id, post_id):

#     place_description = data["comment_li"] #場所ごとのコメント
#     place_review = data["rating_li"] #場所ごとのレーティング
#     booking_url = data["url_li"] #場所ごとの予約URL
#     price = data["price_li"] #場所ごとの価格

    sql = ("SELECT * FROM plan_places WHERE plan_id = %s", (post_id,))
    place_info_li =  get_dict_resultset(*sql)

    sql = (
        """
        SELECT plans.id, plans.user_id, plans.title, plans.description, plans.url, plans.posted_at, users.name
        FROM plans INNER JOIN users ON plans.user_id = users.id WHERE plans.id=%s;
        """
        , (post_id,))

    plan_info = get_dict_resultset(*sql)

    #place_idから緯度経度、URLを取得
    for index, place_info in enumerate(place_info_li):
        #place_idから情報を取得
        response = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_info["place_id"]}&key={map_api_key}').json()
        try:
            place_info_li[index]["url"] = response["result"]["website"]
        except KeyError:
            place_info_li[index]["url"] = "WEBサイトが見つかりません"

        place_info_li[index]["lat"] = response["result"]["geometry"]["location"]["lat"]
        place_info_li[index]["lng"] = response["result"]["geometry"]["location"]["lng"]

        #emojiを表示させたくないtypesを削除
        types_li = response["result"]["types"]

        for type_index, type in enumerate(types_li):
            if type in ["pointofinterest", "tourist_attraction", "establishment"]:
                types_li.pop(type_index)

        # 対応する絵文字がある場合とない場合で分岐
        if types_li[0] in emoji_array:
            place_info_li[index]["types"] = [types_li[0], emoji_array[types_li[0]]]
        else:
            place_info_li[index]["types"] = [types_li[0], "🤟"]

    #ログインしている場合、データベースから情報を取って来て過去にlikeしているかを判定
    if status:
        is_liked = False
        sql = ("SELECT * FROM likes WHERE plan_id = %s AND user_id = %s", post_id, session["id"],)
        like_infomation = get_dict_resultset(*sql)

        #過去にlikeしていない場合
        if like_infomation == []:
            pass
        #過去にlikeしている場合
        else:
            is_liked = True
        #過去のlike状況をフロント側に伝える
        return render_template('content.html', plan_info = plan_info, user_id = session["id"], place_info_li = place_info_li, is_liked=is_liked, status=status, user_name=session["user_name"],  map_api_key = map_api_key)

    else:
        return render_template('content.html', plan_info = plan_info, place_info_li = place_info_li,  map_api_key = map_api_key)


@app.route('/like', methods=['GET', 'POST'])
def like():

    if request.method=="POST":

        dt_now = datetime.datetime.now()

        plan_id = request.json['plan_id']
        user_id = session["id"]

        sql = ("SELECT * FROM likes WHERE plan_id = %s AND user_id = %s", plan_id, user_id,)
        like_info = get_dict_resultset(*sql)

        conn = psycopg2_connect()
        cur = conn.cursor()

        #過去にLikeしたことがない場合、新たに列を追加
        if like_info == []:
            cur.execute("INSERT INTO likes (plan_id, user_id, created_at) VALUES (%s, %s, %s)", (plan_id, user_id, dt_now,))
            conn.commit()
            conn.close()

            sql = ("SELECT * FROM likes WHERE plan_id = %s AND user_id = %s", plan_id, user_id,)
            like_info = get_dict_resultset(*sql)

        #過去にLikeしたことがある場合、データベースから削除
        else:
            cur.execute("DELETE FROM likes WHERE plan_id = %s AND user_id = %s", (plan_id, user_id,))
            conn.commit()
            conn.close()

    return "いいねボタン押後のデータベースの処理が完了しました"

# mypage表示の処理
@app.route("/mypage/<int:user_id>")
@login_required
def mypage(user_id):
    global status

    sql = ("""
        SELECT plans.id, plans.user_id, plans.title, plans.description, plans.url, plans.posted_at, plans.costs, plans.days, users.name
        FROM plans INNER JOIN users ON plans.user_id = users.id WHERE users.id = %s;
        """, (session["id"],))
    plans = get_dict_resultset(*sql)

    sql = ("""
        SELECT plan_id
        FROM likes;
        """,
    )
    likes = get_dict_resultset(*sql)
    # like数カウント
    plan_id_num=[]
    planid_like_dic = {}

    for like in likes:
        plan_id_num.append(like["plan_id"])
    else:
        for plan_id in plan_id_num:
            planid_like_dic[plan_id] = int(plan_id_num.count(plan_id))

    # like数をplansに加える
    for plan_index, plan in enumerate(plans):
        if plan["id"] in planid_like_dic.keys():
            plans[plan_index]["likes"] = planid_like_dic[plan["id"]]

    plans.reverse()

    
    # ユーザ情報を取得
    sql = ("SELECT email, registered_at FROM users WHERE id = %s", (session["id"],))
    users = get_dict_resultset(*sql)
    # 投稿総数を取得
    sql = ("SELECT COUNT(*) AS plans_sum FROM plans WHERE user_id = %s", (session["id"],))
    sum = get_dict_resultset(*sql)
    #urlからyoutubeIDを取得
    for index, plan in enumerate(plans):
        plan["video_id"] = plan["url"].split("/")[3]

    # conn.close()

    #ページネーション機能
    page_info = paginate(plans)
    print(users)
    print(likes)
    return render_template('profile.html', plans=page_info["plans"], CurPage=page_info["CurPage"], MaxPage=page_info["MaxPage"], 
                            status=status, user_name=session["user_name"], email=users[0]["email"], register_date=users[0]["registered_at"], 
                            user_id=session["id"], plans_sum=sum[0]["plans_sum"],  map_api_key = map_api_key)

# mypageでいいね一覧を見る
@app.route("/mypage_likes/<int:user_id>")
@login_required
def mypage_likes(user_id):
    global status

    sql = ("""
    SELECT plans.id, plans.user_id, plans.title, plans.description, plans.url, plans.posted_at, plans.costs, plans.days  
    FROM plans INNER JOIN likes ON plans.id = likes.plan_id WHERE likes.user_id = %s;
    """, (session["id"],))
    plans = get_dict_resultset(*sql)

    sql = (
        """
        SELECT plan_id
        FROM likes;
        """,)
    likes = get_dict_resultset(*sql)

    # like数カウント
    plan_id_num=[]
    planid_like_dic = {}

    for like in likes:
        plan_id_num.append(like["plan_id"])
    else:
        for plan_id in plan_id_num:
            planid_like_dic[plan_id] = int(plan_id_num.count(plan_id))

    # like数をplansに加える
    for plan_index, plan in enumerate(plans):
        if plan["id"] in planid_like_dic.keys():
            plans[plan_index]["likes"] = planid_like_dic[plan["id"]]

    plans.reverse()

    # ユーザ情報を取得
    sql = ("SELECT email, registered_at FROM users WHERE id = %s", (session["id"],))
    users = get_dict_resultset(*sql)
    # いいね総数を取得
    sql = ("SELECT COUNT(*) AS counts FROM likes WHERE user_id = %s", (session["id"],))
    sum = get_dict_resultset(*sql)


    #urlからyoutubeIDを取得
    for index, plan in enumerate(plans):
        plan["video_id"] = plan["url"].split("/")[3]

    #ページネーション機能
    page_info = paginate(plans)

    # conn.close()

    return render_template('profile_likes.html',plans=page_info["plans"], CurPage=page_info["CurPage"], MaxPage=page_info["MaxPage"],
                                                status=status,
                                                user_id=session["id"], user_name=session["user_name"],
                                                email=users[0]["email"], register_date=users[0]["registered_at"],
                                                likes_sum=sum[0]["counts"],  map_api_key = map_api_key)

# ページネーション機能
def paginate(plans):
    # (1) 表示されているページ番号を取得(初期ページ1)
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # (2)１ページに表示させたいデータ件数を指定して分割(１ページに3件表示)
    PageData = plans[(page - 1)*6: page*6]

    # (3) 表示するデータリストの最大件数から最大ページ数を算出
    MaxPage = (- len(plans) // 6) * -1

    page_info = {"plans" : PageData, "CurPage" : page, "MaxPage" : MaxPage}

    return page_info


# 投稿を削除する
@app.route("/delete/<int:plan_id>")
@login_required
def delete(plan_id):
    """
    GET:
    POST: 選択したplanの削除
    """
    # plansテーブル、plan_placesテーブルから削除
    con = psycopg2_connect()
    cur = con.cursor()
    cur.execute("""DELETE FROM likes WHERE id = %s""", str(plan_id))
    cur.execute("""DELETE FROM plan_places WHERE plan_id = %s""", str(plan_id))
    cur.execute("""DELETE FROM plans WHERE id = %s""", str(plan_id))
    con.commit()
    con.close()

    return redirect(url_for("mypage", user_id=session["id"]))


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')

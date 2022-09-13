from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/post')
def post():
    return render_template('post.html')

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
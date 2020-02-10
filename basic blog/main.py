import pymysql
from app import app
from db_config import mysql
from flask import Flask, url_for
from flask import flash, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import get_debug_queries

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/start_session", methods=["POST"])
def start_session():
    msg = ""
    conn = None
    cursor = None
    if (
        request.method == "POST"
        and "email" in request.form
        and "password" in request.form
    ):
        _email = request.form["email"]
        _password = request.form["password"]
        _hashed_password = generate_password_hash(_password)
        sql = "SELECT * FROM users WHERE email = %s"
        data = (_email)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,data)
        account = cursor.fetchone()
        if check_password_hash(account['password'],_password):
            if account:
                session["loggedin"] = True
                session["id"] = account["id"]
                session["uname"] = account["email"]
                # session['username'] = account['username']
                # Redirect to home page
                msg = "Login successfull"
        else:
            # Account doesnt exist or username/password incorrect
            msg = "Incorrect username/password!"
    # Show the login form with message (if any)
    return redirect(url_for('index',msg=msg,**request.args))


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/register_user", methods=["POST"])
def register_user():
    conn = None
    cursor = None
    try:
        _email = request.form["email"]
        _password = request.form["password"]
        _hashed_password = generate_password_hash(_password)
        if _email and _password and request.method == "POST":
            sql = "INSERT INTO users(email,password) VALUES (%s, %s)"
            data = (_email, _hashed_password)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash("User added successfully!!")
            return redirect("/")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/")
def index():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM posts")
        rows = cursor.fetchall()
        return render_template("index.html", rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/new")
def create_post():
    return render_template("create_post.html")


@app.route("/post", methods=["POST"])
def post():
    conn = None
    cursor = None
    try:
        _title = request.form["title"]
        _content = request.form["content"]
        if _title and _content and request.method == "POST":
            sql = "INSERT INTO posts(title,content) VALUES (%s, %s)"
            data = (_title, _content)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash("Post added successfully!!")
            return redirect("/")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    print('=' * 80)
    print(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    print(query_str.rstrip('\n'))
    print('=' * 80 + '\n')

    return response

app.after_request(sql_debug)    



if __name__ == "__main__":
    app.run(debug=True)


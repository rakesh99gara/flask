import pymysql
from db_config import mysql
from flask import Blueprint,render_template,url_for
from flask import flash, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__,template_folder='templates')

@auth.route("/login")
def login():
    return render_template("auth/login.html")


@auth.route("/start_session", methods=["POST"])
def start_session():
    error = ""
    conn = None
    cursor = None
    try:
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
                    return redirect(url_for('home.index'))
            else:
                # Account doesnt exist or username/password incorrect
                error = "Incorrect username/password!"
        # Show the login form with message (if any)
                return render_template('auth/login.html',error = error)
    except Exception as e:
        print(e)
        error = "Incorrect username/password!"
        return render_template('auth/login.html',error = error)
    finally:
        conn.close()
        cursor.close()

@auth.route("/signup")
def signup():
    return render_template("auth/signup.html")


@auth.route("/register_user", methods=["POST"])
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
            success = "SignUp successfull. Login to proceed"
            return render_template('auth/login.html',success=success)
    except Exception as e:
        print(e)
        error = "Email already exists"
        return render_template('auth/signup.html',error=error)
    finally:
        cursor.close()
        conn.close()

@auth.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('uname', None)
   return redirect(url_for('home.index'))



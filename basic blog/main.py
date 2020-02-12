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

@app.route("/a")
def a():
    return render_template("a.html")

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
                return redirect(url_for('index'))

        else:
            # Account doesnt exist or username/password incorrect
            msg = "Incorrect username/password!"
    # Show the login form with message (if any)
            return render_template('login.html',msg = msg)


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
            msg = "SignUp successfull. Login to proceed"
            return render_template('login.html',msg=msg)
    except Exception as e:
        print(e)
        msg = "Email already exists"
        return render_template('signup.html',msg=msg)
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
        cursor.execute("SELECT posts.id, posts.title, posts.content, posts.user_id, users.email FROM posts INNER JOIN users ON posts.user_id = users.id")
        rows = cursor.fetchall()
        return render_template("index.html", rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route("/new")
def create_post():
    if session['loggedin']:
        return render_template("create_post.html")
    else:
        return render_template('login.html',msg="Login to proceed")



@app.route("/post", methods=["POST"])
def post():
    conn = None
    cursor = None
    try:
        _title = request.form["title"]
        _content = request.form["content"]
        if _title and _content and request.method == "POST":
            sql = "INSERT INTO posts(title,content,user_id) VALUES (%s, %s, %s)"
            data = (_title, _content, session['id'])
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

@app.route("/post_comment/<int:post_id>", methods=["POST"])
def post_comment(post_id):
    conn = None
    cursor = None
    try:
        _name = request.form["name"]
        _comment = request.form["comment"]
        if _name and _comment and request.method == "POST":
            sql = "INSERT INTO comments(name,comment,post_id,user_id) VALUES (%s, %s, %s, %s)"
            data = (_name, _comment, post_id, session['id'])
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect(url_for('show',id=post_id))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/show/<int:id>')
def show(id):
    conn = None
    cursor = None
    try:
        sql = "SELECT * FROM posts WHERE id = %s"
        data = (id)
        conn = mysql.connect()
        # cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute(sql, data)
        post = cursor.fetchone()
        sql = "SELECT * FROM users WHERE ID IN ( SELECT user_id FROM posts WHERE id = %s)"
        cursor.execute(sql,data)
        user = cursor.fetchone()
        sql = "SELECT * FROM comments where post_id = %s"
        cursor.execute(sql,data)
        comments = cursor.fetchall()
        return render_template('show_post.html',post = post,comments = comments, user = user)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/delete_comment/<int:post_id>/<int:comment_id>')
def delete_comment(post_id,comment_id):
    conn = None
    cursor = None
    try:
        sql = "DELETE FROM comments where id = %s"
        data = (comment_id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('show',id=post_id))
    
    
@app.route('/edit_post/<int:id>')
def edit_post(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM posts WHERE id = %s",id)
        row = cursor.fetchone()
        if row:
            return render_template('edit_post.html',row=row)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()            

@app.route('/delete_post/<int:id>')
def delete_post(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "DELETE FROM comments where post_id = %s"
        data = (id)
        cursor.execute(sql,data)
        conn.commit()
        sql = "DELETE FROM posts where id = %s"
        cursor.execute(sql,data)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/update_post/<int:id>',methods=['POST'])
def update_post(id):
    conn = None
    cursor = None
    try:
        _title = request.form['title']
        _content = request.form['content']
        if _title and _content and request.method == 'POST':
            sql = "UPDATE posts SET title = %s, content = %s where id = %s"
            data = (_title,_content,id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql,data)
            conn.commit()
            return redirect(url_for('show',id=id))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()        

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('uname', None)
   # Redirect to login page
   return redirect(url_for('index'))

# def sql_debug(response):
#     queries = list(get_debug_queries())
#     query_str = ''
#     total_duration = 0.0
#     for q in queries:
#         total_duration += q.duration
#         stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
#         query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

#     print('=' * 80)
#     print(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
#     print('=' * 80)
#     print(query_str.rstrip('\n'))
#     print('=' * 80 + '\n')

#     return response

# app.after_request(sql_debug)    



if __name__ == "__main__":
    app.run(debug=True)


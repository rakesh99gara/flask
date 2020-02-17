import pymysql
from app import app
from db_config import mysql
from flask import Flask, url_for
from flask import flash, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import get_debug_queries

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/a")
def a():
    return render_template("a.html")

@app.route("/start_session", methods=["POST"])
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
                    return redirect(url_for('index'))
            else:
                # Account doesnt exist or username/password incorrect
                error = "Incorrect username/password!"
        # Show the login form with message (if any)
                return render_template('login.html',error = error)
    except Exception as e:
        print(e)
        error = "Incorrect username/password!"
        return render_template('login.html',error = error)
    finally:
        conn.close()
        cursor.close()

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
            success = "SignUp successfull. Login to proceed"
            return render_template('login.html',success=success)
    except Exception as e:
        print(e)
        error = "Email already exists"
        return render_template('signup.html',error=error)
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
        return render_template('login.html',error="Login to proceed")



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

@app.route('/users')
def users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT users.id, users.email, count( posts.id ) AS no_of_posts, users.created_at FROM users LEFT JOIN posts ON users.id = posts.user_id GROUP BY users.id ORDER BY 4 DESC ")       
        users = cursor.fetchall()
        return render_template("users.html", users=users)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/view_user/<int:id>')
def view_user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT posts.id, posts.title, posts.content, count(comments.id) AS no_of_comments, posts.created_at, posts.updated_at FROM posts LEFT JOIN comments ON posts.id = comments.post_id WHERE posts.user_id = %s GROUP BY posts.id",id)
        user_posts = cursor.fetchall()
        cursor.execute("SELECT * from users WHERE id = %s", id)
        user = cursor.fetchone()
        return render_template("view_user.html",user_posts = user_posts,user = user)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/profile/<int:id>')
def profile(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE id = %s",id)
        user_profile = cursor.fetchone()
        cursor.execute("SELECT posts.id, posts.title, posts.content, count( comments.id ) AS no_of_comments, posts.created_at, posts.updated_at FROM posts LEFT JOIN comments ON posts.id = comments.post_id WHERE posts.user_id = %s GROUP BY posts.id",id)
        user_posts = cursor.fetchall()
        cursor.execute("SELECT comments.id, comments.name, comments.comment, posts.id as post_id, posts.title, comments.created_at FROM comments LEFT JOIN posts ON posts.id = comments.post_id WHERE comments.user_id = %s",id)
        user_comments = cursor.fetchall()
        cursor.execute("SELECT count(id) as no_of_posts FROM posts WHERE user_id = %s",id)
        user_no_posts = cursor.fetchone()
        cursor.execute("SELECT count(id) as no_of_comments FROM comments WHERE user_id = %s",id)
        user_no_comments = cursor.fetchone()
        return render_template("profile.html",user_posts = user_posts,user_profile = user_profile,user_comments = user_comments,user_no_posts = user_no_posts,user_no_comments=user_no_comments)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return render_template('profile.html')

@app.route('/change_profile/<int:id>')    
def change_profile(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE id = %s",id)
        user_details = cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()        
    return render_template('change_profile.html',user_details = user_details)

@app.route('/update_profile/<int:id>',methods=['POST'])
def update_profile(id):
    conn = None
    cursor = None
    if (
        request.method == "POST"
        and "email" in request.form
        and "current_password" in request.form
    ):
        _email = request.form["email"]
        _new_password = request.form["new_password"]
        _current_password = request.form['current_password']
        _hashed_current_password = generate_password_hash(_current_password)
        _hashed_new_password = generate_password_hash(_new_password)
        sql = "SELECT * FROM users WHERE id = %s"
        data = (id)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,data)
        account = cursor.fetchone()
        if check_password_hash(account['password'],_current_password):
            if account:
                if _new_password != '':
                    try:
                        sql = "UPDATE users SET email = %s, password = %s where id = %s"
                        data = (_email, _hashed_new_password,id)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sql, data)
                        conn.commit()
                        sql = "SELECT * FROM users WHERE id = %s"
                        data = (id)
                        cursor.execute(sql,data)
                        account = cursor.fetchone()
                        session["loggedin"] = True
                        session["id"] = account[0]
                        session["uname"] = account[1]
                        return redirect(url_for('profile',id=id))
                    except Exception as e:
                        print(e)
                        return render_template("change_profile.html",user_details = account,error="Email already Exists")
                    finally:
                        conn.close()
                        cursor.close()
                else:
                    try:
                        sql = "UPDATE users SET email = %s, password = %s where id = %s"
                        data = (_email, _hashed_current_password,id)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sql, data)
                        conn.commit()
                        sql = "SELECT * FROM users WHERE id = %s"
                        data = (id)
                        cursor.execute(sql,data)
                        account = cursor.fetchone()
                        session["loggedin"] = True
                        session["id"] = account[0]
                        session["uname"] = account[1]
                    except Exception as e:
                        print(e)
                        return render_template("change_profile.html",user_details = account,error="Email already Exists")
                    finally:
                        conn.close()
                        cursor.close()

        else:
            error = "Incorrect current password!"
            return render_template('change_profile.html',user_details = account,error = error)
    return redirect(url_for('profile',id=id))


@app.route('/delete_profile/<int:id>')
def delete_profile(id):
    conn = None
    cursor = None
    try:
            sql = "SELECT * FROM users WHERE id = %s"
            data = (id)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql,data)
            account = cursor.fetchone()
            if account:
                sql = "DELETE FROM comments WHERE post_id IN (  SELECT id FROM posts WHERE user_id = %s )"
                data = (id)
                cursor.execute(sql,data)
                conn.commit()
                sql = "DELETE FROM posts WHERE user_id = %s"
                data = (id)
                cursor.execute(sql,data)
                conn.commit()
                sql = "DELETE FROM users WHERE id = %s"
                data = (id)
                cursor.execute(sql,data)
                conn.commit()
                session.pop('loggedin', None)
                session.pop('id', None)
                session.pop('uname', None)
                return redirect(url_for('index',success = "Profile deleted Successfully"))
    except Exception as e:
        print(e)
    finally:
        conn.close()
        cursor.close()



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


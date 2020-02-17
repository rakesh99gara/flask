import pymysql
from db_config import mysql
from flask import Blueprint,render_template,url_for
from flask import flash, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash



users = Blueprint('users',__name__,template_folder="templates")

@users.route('/all_users')
def all_users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ("SELECT users.id, users.email, count(posts.id) AS no_of_posts, users.created_at From users LEFT JOIN posts ON users.id = posts.user_id GROUP BY users.id ORDER BY 4 DESC")
        users = cursor.fetchall()
        return render_template("users/users.html",users = users)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@users.route('/view_user/<int:id>')
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
        return render_template("users/view_user.html",user_posts = user_posts,user = user)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@users.route('/profile/<int:id>')
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
        return render_template("users/profile.html",user_posts = user_posts,user_profile = user_profile,user_comments = user_comments,user_no_posts = user_no_posts,user_no_comments=user_no_comments)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return render_template('profile.html')

@users.route('/change_profile/<int:id>')    
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
    return render_template('users/change_profile.html',user_details = user_details)

@users.route('/update_profile/<int:id>',methods=['POST'])
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
                        return redirect(url_for('users.profile',id=id))
                    except Exception as e:
                        print(e)
                        return render_template("users/change_profile.html",user_details = account,error="Email already Exists")
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
                        return render_template("users/change_profile.html",user_details = account,error="Email already Exists")
                    finally:
                        conn.close()
                        cursor.close()

        else:
            error = "Incorrect current password!"
            return render_template('users/change_profile.html',user_details = account,error = error)
    return redirect(url_for('profile',id=id))


@users.route('/delete_profile/<int:id>')
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
                sql = "DELETE FROM comments WHERE user_id = %s"
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
                return redirect(url_for('home.index',success = "Profile deleted Successfully"))
    except Exception as e:
        print(e)
    finally:
        conn.close()
        cursor.close()
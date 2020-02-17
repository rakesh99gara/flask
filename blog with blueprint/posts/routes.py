import pymysql
from db_config import mysql
from flask import Blueprint,url_for
from flask import flash, render_template, request, redirect, session

posts = Blueprint('posts',__name__,template_folder='templates')

@posts.route("/new")
def create_post():
    if session['loggedin']:
        return render_template("posts/create_post.html")
    else:
        return render_template('auth/login.html',error="Login to proceed")



@posts.route("/post", methods=["POST"])
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

@posts.route("/post_comment/<int:post_id>", methods=["POST"])
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
            return redirect(url_for('posts.show',id=post_id))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@posts.route('/show/<int:id>')
def show(id):
    conn = None
    cursor = None
    try:
        sql = "SELECT * FROM posts WHERE id = %s"
        data = (id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        post = cursor.fetchone()
        sql = "SELECT * FROM users WHERE ID IN ( SELECT user_id FROM posts WHERE id = %s)"
        cursor.execute(sql,data)
        user = cursor.fetchone()
        sql = "SELECT * FROM comments where post_id = %s"
        cursor.execute(sql,data)
        comments = cursor.fetchall()
        return render_template('posts/show_post.html',post = post,comments = comments, user = user)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@posts.route('/delete_comment/<int:post_id>/<int:comment_id>')
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
    return redirect(url_for('posts.show',id=post_id))
    
    
@posts.route('/edit_post/<int:id>')
def edit_post(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM posts WHERE id = %s",id)
        row = cursor.fetchone()
        if row:
            return render_template('posts/edit_post.html',row=row)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()            

@posts.route('/delete_post/<int:id>')
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
    return redirect(url_for('main.index'))

@posts.route('/update_post/<int:id>',methods=['POST'])
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
            return redirect(url_for('posts.show',id=id))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close() 

import pymysql
from db_config import mysql
from flask import Blueprint,render_template,url_for
home = Blueprint('home',__name__,template_folder='templates')

@home.route("/")
def index():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT posts.id, posts.title, posts.content, posts.user_id, users.email FROM posts INNER JOIN users ON posts.user_id = users.id")
        rows = cursor.fetchall()
        return render_template("home/index.html", rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    # return render_template("home/index.html")

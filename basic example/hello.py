import pymysql
from db_config import mysql
from flask import render_template
from flask import Flask,url_for
app = Flask(__name__)
@app.route('/')
def index():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user")
		rows = cursor.fetchall()
		return render_template('index.html', rows=rows)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
    # return render_template('index.html')



@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# @app.route('/projects/')
# def projects():
#     return 'this is projects page'

# @app.route('/about')
# def about():
#     return 'this is about'
with app.test_request_context():
    url_for('static',filename='style.css')

if __name__ == '__main__':
   app.run()
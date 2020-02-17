import pymysql
from app import app
from db_config import mysql
from flask import Flask, url_for,Blueprint
from flask import flash, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import get_debug_queries
from auth.routes import auth
from posts.routes import posts
from home.routes import home
from users.routes import users

app.register_blueprint(auth)
app.register_blueprint(posts)
app.register_blueprint(home)
app.register_blueprint(users)


if __name__ == "__main__":
    app.run(debug=True)


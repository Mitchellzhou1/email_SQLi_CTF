# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors


# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host="127.0.0.1",
                       port=3306,
                       user='root',
                       password='',
                       db='user_enum_ctf',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# Import Flask Library
import string, random
from flask import Flask, render_template, request, session, url_for, redirect, make_response
import pymysql.cursors

app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host="127.0.0.1",
                       port=3306,
                       user='root',
                       password='',
                       db='email_sqli_ctf',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)



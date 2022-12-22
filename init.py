from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from app import app, conn
import login



app.secret_key = 'Q3I3Pm1lc3Np'

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
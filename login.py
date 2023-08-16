from app import *
import string, random
from flask import Flask, make_response, make_response
import re
 
def generate_cookie(length = 20):
    characters = string.ascii_letters + string.digits  # Includes both letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    session['trackingID'] = random_string
    return random_string


def validEmail(email):
    regex = "^[a-zA-Z0-9-_!#$%&'*+-/=?^_`{|}~']+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.search(regex, email)


@app.route('/')
def login(email = '', password = ''):
    name = ''
    cursor = conn.cursor()

    if email and password:
        if validEmail(email):
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))

            user = cursor.fetchone()

            if not user:
                message = "Sorry, this user is doesn't exist"
                return render_template('login.html', error=message)
            else:
                name = user['name']
                session['email'] = user['email']
                
                
    cursor.close()
    res = make_response(render_template('userHome.html', welcome = name, flag = True))

    return res


@app.route('/login', methods = ["POST"])
def loginPage():
    return render_template('login.html')


@app.route('/logout', methods = ["POST"])
def logout():
    message = ''
    try:
        session.pop('email')
        message = 'You have Successfully Logged Out'
    except Exception:
        message = ''
    return render_template('userHome.html', welcome = message, flag = False)


@app.route('/submit', methods = ["POST"])
def submit():
    email = request.form['email']
    password = request.form['password']
    return login(email, password)


# @app.route('/userHome', methods = ["POST"])
# def openHomePage():
#     try:
#         name = session['name']
#         return render_template('userHome.html', welcome = name)
#     except Exception:
#         pass
#         return render_template('userHome.html', welcome = name)
    


from app import *
import string, random
from flask import Flask, make_response, make_response
import re
 

def printSession():
    print(f"""



        SESSION : {session}



""")

def generate_cookie(length = 20):
    characters = string.ascii_letters + string.digits  # Includes both letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    session['trackingID'] = random_string
    printSession()
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
                
    res = make_response(render_template('userHome.html', welcome = name, flag = True))

    if 'trackingID' not in session:
        res.set_cookie("trackingID", generate_cookie())
        query = "INSERT INTO trackingID (cookie, email) VALUES (%s, %s)"
        cursor.execute(query, (session['trackingID'], 'guest'))
        conn.commit()

    else:
        cookie = request.cookies.get("trackingID")
        query = f"SELECT * FROM trackingid WHERE cookie='{cookie}';"
        print('\n' * 10, query, '\n' * 10)
        try:
            cursor.execute(query)
            badSQLflag = False
            result = cursor.fetchone()
        except Exception:
            badSQLflag = True
            result = None

        #print("\n\n\n", result)
        session['trackingID'] = cookie
        if not result or badSQLflag:
            # entering invalid cookie will cause the session email to be None
            session['email'] = 'Error'
        else:
            session['email'] = result['email']
        query = 'UPDATE trackingid SET email = %s WHERE cookie = %s'
        cursor.execute(query, (email, cookie))           

    cursor.close()
    #printSession()
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

from app import *
    


@app.route('/')
def login(email = '', password = ''):

    cursor = conn.cursor()

    if not email and not password:
        return render_template('login.html')

    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))

    user = cursor.fetchone()
    cursor.close()
    if user:
        session['email'] = email
        session['ID'] = user['userID']
        return render_template('userHome.html', name = user['name'], email=user['email'], ID=user['userID'])
    message = "Sorry, the creditials are incorrect"

    return render_template('login.html', error=message)



@app.route('/home', methods = ["POST"])
def submit():
    email = request.form['email']
    password = request.form['password']
    return login(email, password)


@app.route('/home/{{userID}}', methods = ["POST"])
def getUser(userID):
    cursor = conn.cursor()
    session['ID'] = userID
    query = "SELECT * FROM users WHERE userID = %s"
    cursor.execute(query, (userID))

    user = cursor.fetchone()

    if user:
        return render_template('userHome.html', name = user['name'], email=user['email'], ID=user['userID'])
    else:
        message = "Sorry, that person doesn't exist in our database"
        return render_template('login.html', error=message)
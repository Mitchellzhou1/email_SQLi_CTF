from app import *
import re
 
  
def validEmail(email):
    regex = "^[a-zA-Z0-9-_!#$%&'*+-/=?^_`{|}~']+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.search(regex, email)

    


@app.route('/')
def login(email = '', password = ''):

    cursor = conn.cursor()

    if not email and not password:
        return render_template('login.html')
    
    message = "You have entered an invalid email"
    if validEmail(email):
        # only the email parameter is injectable
        query = "SELECT * FROM users WHERE email = '" + email + "' AND password = %s"
        cursor.execute(query, (password))

        user = cursor.fetchone()
        if user:
            session['email'] = email
            return render_template('userHome.html', name = user['name'], email=user['email'], phone=user['phone'])
        message = "Sorry, this user is doesn't exist"

    cursor.close()
    return render_template('login.html', error=message)



@app.route('/submit', methods = ["POST"])
def submit():
    email = request.form['email']
    password = request.form['password']
    return login(email, password)


@app.route('/userHome', methods = ["POST"])
def openHomePage():
    try:
        email = session['email']
    except Exception:
        message = 'Please Login or Create an Account'
        return render_template('login.html', error=message)
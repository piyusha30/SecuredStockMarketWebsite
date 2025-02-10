from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
  
app = Flask(__name__, static_url_path='/static')
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root*123'
app.config['MYSQL_DB'] = 'StockMarketData'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

       # cursor.execute("SELECT * FROM Trader WHERE name ='%s' AND password ='%s'" % (name, password, ))
        cursor.execute("SELECT * FROM Trader WHERE name = %s AND password = %s", (name, password))

        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct name / password !'
    return render_template('login.html', mesage = mesage)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Trader WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            #cursor.execute('INSERT INTO Trader VALUES (% s, % s, % s)', (userName, email, password, ))
            cursor.execute('INSERT INTO Trader (name, email, password) VALUES (%s, %s, %s)', (userName, email, password,))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)
    
if __name__ == "__main__":

    #app.run(ssl_context=("cert.pem","key.pem")) 
    app.run(host='0.0.0.0', port=5000, ssl_context=("cert.pem", "key.pem"))
   # app.run(host="0.0.0.0",port=50100,debug=True, ssl_context="adhoc") #dummy ssl certificate
    # app.run(host="0.0.0.0",port=50100,debug=True, ssl_context=("cert.pem","key.pem")) 
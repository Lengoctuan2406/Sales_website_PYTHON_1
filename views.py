from flask import * 
from flask_mysqldb import MySQL
import MySQLdb.cursors
from function import *
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

app.secret_key = "admin"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'meow_shop'
 
mysql = MySQL(app)

@app.route('/')
@app.route('/_users/index')
def index():
    return render_template('_users/index.html')
@app.route('/_users/login')
def login():
    return render_template('_users/login.html')
@app.route('/_users/register')
def register():
    return render_template('_users/register.html')

@app.route('/_users/login/check_form', methods = ['POST', 'GET'])
def login_check():
    msg = ''
    if request.method == 'POST' and 'login' in request.form:
        email = request.form['email']
        password = request.form['password']
        #kiểm tra email và password có hợp lệ
        if(not validate_email(email) or not validate_password(password)):
            msg = 'Email or password arent allowed!'
            return render_template('_users/login.html', msg=msg)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['account_id'] = account['account_id']
            session['account_name'] = account['account_name']
            session['avatar'] = account['avatar']
            msg = 'Logged in successfully!'
            return redirect(url_for('index'), Response=msg)
        else:
            msg = 'Incorrect email or password!'
            return redirect(url_for('login'), msg=msg)
        #return redirect(url_for('_users/register'), msg=msg)

    # if(check_login()):
    #     return render_template('_users/register.html')
    # else:
    #     msg = 'You must be login first!'
    #     return render_template('_users/login.html', msg=msg)

if __name__=='__main__':
    app.run(host='localhost', port=5000)
from flask import Flask, render_template, request, session, g
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vijay'
app.config['MYSQL_DB'] = 'new_schema'

mysql = MySQL(app)
UserData = []

@app.route('/')
def Home():
    return render_template('/Signin.html')
@app.route('/signin', methods =['GET', 'POST'])
def signin():
    g = ''
    if request.method == 'POST':
        session.pop('user',None)
        username = request.form['username']
        password = request.form['password']
        print(username)
        #print(username,password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(cursor.execute('SELECT * FROM userdetails WHERE email=%s and password=%s',(username,password)))
        #select * from userdetails where emailid='nihar123@gmail.com' and password='123'
        authenticate = cursor.fetchone()

        if authenticate:
            session['username']=authenticate['EMAIL']
            session['password']=authenticate['PASSWORD']
            user = authenticate['EMAIL']

            g="login successful"
            cursor.execute('SELECT * FROM doctordetails')

            UserData=cursor.fetchall()

            return render_template('Home.html',user=session['username'] , UserData=UserData)
        else:
            g='invalid username and password'
            return "invalid password or email"
    return render_template('Signin.html')
@app.route('/Signup11',methods=['GET','POST'])
def signup11():
    return render_template('Signup.html')


@app.route('/Signup',methods=['GET','POST'])
def Signup():
    g=''
    if request.method=='POST':
        username=request.form['name']
        email=request.form['username']
        password=request.form['password']
        contact=request.form['contact']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(cursor.execute('SELECT * FROM userdetails WHERE email=%s', (email,)))
        account = cursor.fetchone()
        print(account)
        if account:
            g= 'Account already exists !'
        else:
            cursor.execute('INSERT INTO userdetails VALUES (%s,%s,%s,%s)', (username,email,password,contact))
            mysql.connection.commit()
            g = 'You have successfully registered !'

    return render_template('Signin.html', msg=g)

@app.route('/display',methods=['GET'])
def display():
    if session['username']:
       # print(session['username'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #print(cursor.execute('SELECT * FROM userdetails WHERE email=%s ',(session['username'],)))
        cursor.execute('SELECT * FROM userdetails WHERE email=%s ',(session['username'],))
        disp=cursor.fetchone()
        print(disp)
        return render_template('manageaccount.html',username=disp['EMAIL'],password=disp['PASSWORD'],name=disp['USERNAME'],contact=disp['CONTACT'])
    #return render_template('Home.html')
@app.before_request
def before_request():
    g.username=None
    if 'username' in session:
       # print(session['username'])
        g.user=session['username']


@app.route('/update',methods=('GET','POST'))
def update():
      #and loggedin in session
        print(request.args,session['username'])
        email = request.args.get("username")
        print(email)
        password = request.args.get("password")
        username = request.args.get("name")
        print(username)
        contact = request.args.get("contact")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #cursor.execute("UPDATE userdetails SET username = %s, email = %s,contact = %d, password = %s WHERE email = %s", (username,email,contact,password))
        if username:
            #print(cursor.execute("UPDATE userdetails SET username = %s, email = %s,contact = %s, password = %s WHERE email = %s", (username,email,contact,password))
#)
            cursor.execute("UPDATE userdetails SET username = %s, email = %s,contact = %s, password = %s WHERE email = %s", (username,email,contact,password,email))

            mysql.connection.commit()
      #g="Updated the user account successfully"
    #flash(g)
        return render_template('Home.html',user=session['username'] ,UserData=UserData)


@app.route("/search",methods=['POST','GET'])
def search():

    SearchKey = request.form.get('searchkey')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM doctordetails')
    UserData = cursor.fetchall()

    SearchData = []

    for Doctor in UserData:
        if SearchKey.lower() in Doctor["specialization"].lower():
            SearchData.append(Doctor)

    return render_template('Home.html', user=session['username'] ,UserData=SearchData)

@app.route("/drop",methods=['post','get'])
def drop():
    session.pop('user',None)
    return render_template('Signin.html')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.secret_key='vijay'
    app.run(debug=True,port=3000)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

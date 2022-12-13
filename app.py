import os
import sqlite3

from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from accounts import AllUser
from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

login_manager = LoginManager(app)
login_manager.login_view = "login"

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath("database.sqlite3"))
    db_path = os.path.join(BASE_DIR, "database.sqlite3")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@login_manager.user_loader
def load_user(user_id):
   conn = get_db_connection();
   curs = conn.cursor()
   curs.execute("SELECT * from AllUser where ID = (?)",[user_id])
   user = curs.fetchone()
   if user is None:
      return None
   else:
      return AllUser(int(user[0]), user[1], user[4], user[2], user[3])

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        conn = get_db_connection()
        email = request.form['email']
        password = request.form['password']

        cur = conn.cursor()
        cur.execute("SELECT * FROM AllUser WHERE email = ?", (email,))
        user = cur.fetchone()
        if (user is None):
            flash('No user with email found')
            return render_template("signin.html")

        user = list(user)

        if user[1] == email and user[4] == password:
            userIn = AllUser(user[0], user[1], user[4], user[2], user[3])
            login_user(userIn)
            msg = 'Successfully logged in: ', current_user.getEmail() , " " , current_user.getFirstName() , " " , current_user.getLastName()
            flash(msg)
            return render_template("account-settings.html")
        else:
            flash('fail')
            return render_template("signin.html")

    return render_template("signin.html")



@app.route('/')
def index():
    conn = get_db_connection()
    conn.close()
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template("search.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        conn = get_db_connection()
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        cur = conn.cursor();

        cur.execute("SELECT * FROM AllUser WHERE email = ?", (email,))

        if cur.fetchone() is not None:

            flash("That email is already taken...")
            conn.close()
            return render_template('signup.html')

        else:
            conn.execute("INSERT INTO AllUser (firstname,lastname,email,password) VALUES (?,?,?,?)",(firstname,lastname,email,password))
            conn.commit()
            flash('SUCCESS, Please log in')
            conn.close()
            return render_template("signin.html")

    return render_template('signup.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('signin.html')

@app.route('/product')
def product():
    return render_template("product.html")

@app.route('/setting')
def setting():

    return render_template("account-settings.html")

@app.route('/orders')
def orders():
    return render_template("account-order.html")

@app.route('/address')
def address():
    return render_template("account-address.html")

@app.route('/payment')
def payment():
    return render_template("account-payment.html")


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)

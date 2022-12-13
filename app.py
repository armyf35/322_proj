from distutils.command import upload
import os
import sqlite3
from accounts import OrdinaryUser
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from accounts import AllUser
from flask import Flask, flash, redirect, url_for, render_template, request, session

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
   conn.close()
   if user is None:
      return None
   else:
      return OrdinaryUser(int(user[0]), user[1], user[4], user[2], user[3])

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        conn = get_db_connection()
        email = request.form['email']
        password = request.form['password']

        cur = conn.cursor()
        cur.execute("SELECT * FROM AllUser WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
        if (user is None):
            flash('No user with email found')
            return render_template("signin.html")

        user = list(user)

        if user[1] == email and user[4] == password:
            userIn = OrdinaryUser(user[0], user[1], user[4], user[2], user[3])
            login_user(userIn)
            msg = 'Successfully logged in: ', current_user.getEmail() , " " , current_user.getFirstName() , " " , current_user.getLastName()
            flash(msg)
            # return render_template("account-settings.html")
            return redirect(url_for('index'))
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
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM Item').fetchall()
    conn.close()
    return render_template("search.html", products=products)


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
            # return render_template("signin.html")
            return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    # return render_template('signin.html')
    return redirect(url_for('signin'))



@app.route('/createItem')
def createItem():
    if request.method == 'POST':
        title = request.form['title']
        productImage = request.files['Product Image']
        price = request.form['price']
        productImage.save(secure_filename(productImage.filename))

        ownerID = current_user.getID

        if not title:
            flash('Title is required!')
        elif not productImage:
            flash('Image is required!')
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO Item (ownerID,Title,startPrice) VALUES (?,?)",(ownerID,title,price))
            conn.commit()

            cur = conn.cursor();
            cur.execute("SELECT * FROM Item WHERE ID = (SELECT MAX(ID)  FROM Item)")
            item = list(cur.fetchone())
            

            conn.execute("INSERT INTO ItemFilePicture(FileName, ItemID) VALUES (?,?)",(ownerID,item[0]))
            
            flash('SUCCESS, PLease see Index')
            conn.close()

    return render_template('createItem.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
        title = request.form['title']
        productImage = request.files['file']
        price = request.form['price']
        imagePic = "https://support.apple.com/library/content/dam/edam/applecare/images/en_US/iphone/iphone-14-pro-max-colors.png"

        ownerID = 1
        #ownerID = current_user.getID
        if not title:
            flash('Title is required!')
        elif not productImage:
            flash('Image is required!')
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO Item (ownerID,Title, StartPrice, FileName) VALUES (?,?,?,?)",(ownerID,title, price,imagePic))
            conn.commit()

            
            flash('SUCCESS, PLease see Index')
            conn.close()
        return render_template("account-payment.html")


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

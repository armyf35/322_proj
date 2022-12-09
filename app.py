import sqlite3
from flask import Flask, flash, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

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

        conn.execute("INSERT INTO AllUser (firstname,lastname,email,password) VALUES (?,?,?,?)",(firstname,lastname,email,password))
        conn.commit()

        flash('SUCCESS, Please log in')
        conn.close()

        return render_template("signin.html")
    else:
        flash('FAILURE to sign up')
        return render_template('signup.html')

        

@app.route('/signin')
def signin():
    return render_template("signin.html")

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

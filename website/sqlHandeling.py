import mysql.connector as sql
from datetime import datetime

from flask import flash, session

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user

db = sql.connect(
    host = "localhost",
    user =  "root",
    passwd = "AppleJack20",
    database = "horizonTravels"
)

cursor = db.cursor()





#cursor.execute("CREATE TABLE Users (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(100), last_name VARCHAR(50), email VARCHAR(150), password VARCHAR(255), phone VARCHAR(15), address VARCHAR(255), zip VARCHAR(15),  date_created DATETIME )")


def insertUser(first_name1, last_name1, email1, password1, DoB, phone1, address1, zip1):
    datenow = (str)(datetime.now().strftime('%Y-%m-%d'))

    date_of_birth1 = (str)(DoB.strftime('%Y-%m-%d'))



    password2 = generate_password_hash(password1, method='sha256')

    cursor.execute("INSERT INTO Users (first_name, last_name, email, password, date_of_birth , phone, address, zip, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (first_name1, last_name1, email1, password2, date_of_birth1, phone1, address1, zip1, datenow))
    db.commit()
    print(cursor.rowcount, "record inserted.")


def dropUserRecord_byID(userID):
    cursor.execute("DELETE FROM Users WHERE id = %s", (userID,))
    db.commit()
    print(cursor.rowcount, "record deleted.")

def dropUserRecord_byEmail(email):
    cursor.execute("DELETE FROM Users WHERE email = %s", (email,))
    db.commit()
    print(cursor.rowcount, "record deleted.")


def getUserRecord_byID(userID):
    cursor.execute("SELECT * FROM Users WHERE id = %s", (userID,))
    user = cursor.fetchone()
    return user

def getUserRecord_byEmail(email):
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()
    return user

def startSession(user):
    if user:
        session['loggedin'] = True
        session['userID'] = user[0]
        session['firstName'] = user[1]
        flash('Logged in successfully!', category='success')

def stopSession():
    session.pop('loggedin', None)
    session.pop('userID', None)
    session.pop('firstName', None)
    flash('Logged out successfully!', category='success')


def loginHelperEmail(email):
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if user:
        return user
    else:
        return False


def userLogin(email, password):
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if user:
        if check_password_hash(user[4], password):
            startSession(user)
            return True
            
        else:
            flash('Incorrect password, try again.', category='error')
            return False
    else:
        flash('Email does not exist.', category='error')
        return False


cursor.execute("SELECT * FROM Users")
#cursor.execute("DESCRIBE Users")

for x in cursor:
    print(x)

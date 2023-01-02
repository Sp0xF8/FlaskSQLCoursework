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

#cursor.execure("CREATE TABLE Flights (id INT AUTO_INCREMENT PRIMARY KEY, departure VARCHAR(100), destination VARCHAR(50), departure_time time, arrival_time time, price float(3))")




##
##
#####  FLIGHT HANDLING
##
##

class Flight:
        ## Create a new flight schedule
    def insertFlight(departure1, destination1, departure_time1, arrival_time1, price1):
        cursor.execute("INSERT INTO Flights (departure, destination, departure_time, arrival_time, price) VALUES (%s, %s, %s, %s, %s)", (departure1, destination1, departure_time1, arrival_time1, price1))
        db.commit()
        print(cursor.rowcount, " Flight record inserted.")


        ## Returns an array of all flights
    def getFlights():
        cursor.execute("SELECT * FROM Flights")
        result = cursor.fetchall()
        return result


        ## Returns a single flight with the given id
    def getFlight(id):
        cursor.execute("SELECT * FROM Flights WHERE id = %s", (id,))
        result = cursor.fetchone()
        return result


        ## Returns an array of flights with the given departure and destination
    def getFlightFromTo(departure, destination):
        cursor.execute("SELECT * FROM Flights WHERE departure = %s AND destination = %s", (departure, destination))
        result = cursor.fetchall()
        return result


        ## Returns an array of flights with the given departure
    def getFlightFrom(departure):
        cursor.execute("SELECT * FROM Flights WHERE departure = %s", (departure,))
        result = cursor.fetchall()
        return result


        ## Returns an array of flights with the given destination
    def getFlightTo(destination):
        cursor.execute("SELECT * FROM Flights WHERE destination = %s", (destination,))
        result = cursor.fetchall()
        return result


        ## Deleted a flight with the given id
    def deleteFlight(id):
        cursor.execute("DELETE FROM Flights WHERE id = %s", (id,))
        db.commit()
        print(cursor.rowcount, " Flight record deleted.")





##
##
#####  USER HANDLING
##
##

class User:

    def insertUser(first_name1, last_name1, email1, password1, DoB, phone1, address1, zip1):
        datenow = (str)(datetime.now().strftime('%Y-%m-%d'))

        date_of_birth1 = (str)(DoB.strftime('%Y-%m-%d'))



        password2 = generate_password_hash(password1, method='sha256')

        cursor.execute("INSERT INTO Users (first_name, last_name, email, password, date_of_birth , phone, address, zip, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (first_name1, last_name1, email1, password2, date_of_birth1, phone1, address1, zip1, datenow))
        db.commit()
        print(cursor.rowcount, "User record inserted.")


    def dropUserRecord_byID(userID):
        cursor.execute("DELETE FROM Users WHERE id = %s", (userID,))
        db.commit()
        print(cursor.rowcount, "User record deleted.")

    def dropUserRecord_byEmail(email):
        cursor.execute("DELETE FROM Users WHERE email = %s", (email,))
        db.commit()
        print(cursor.rowcount, "User record deleted.")


    def getUserRecord_byID(userID):
        cursor.execute("SELECT * FROM Users WHERE id = %s", (userID,))
        user = cursor.fetchone()
        return user

    def getUserRecord_byEmail(email):
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user

    def getAllUsers():
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        return users

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
                User.startSession(user)
                return True
                
            else:
                flash('Incorrect password, try again.', category='error')
                return False
        else:
            flash('Email does not exist.', category='error')
            return False

    def isAdmin():
        if session.get('loggedin'):
            if session.get('userID') == 1:
                return True
            else:
                return False
        else:
            return False

    def isLoggedin():
        if session.get('loggedin'):
            return True
        else:
            return False


    cursor.execute("SELECT * FROM Users")
    #cursor.execute("DESCRIBE Users")

    for x in cursor:
        print(x)

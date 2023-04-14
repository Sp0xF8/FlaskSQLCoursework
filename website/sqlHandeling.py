import mysql.connector as sql
from datetime import datetime

from flask import flash, session

from werkzeug.security import generate_password_hash, check_password_hash


db = sql.connect(
    host = "localhost",
    user =  "root",
    passwd = "AppleJack20",
    database = "horizonTravels"
)

cursor = db.cursor()





#cursor.execute("CREATE TABLE Users (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(100), last_name VARCHAR(50), email VARCHAR(150), password VARCHAR(255), phone VARCHAR(15), address VARCHAR(255), zip VARCHAR(15),  date_created DATETIME )")

#cursor.execure("CREATE TABLE Flights (id INT AUTO_INCREMENT PRIMARY KEY, departure VARCHAR(100), destination VARCHAR(50), departure_time time, arrival_time time, price float(3))")


#curser.execute('CREATE TABLE Tickets ( id int NOT NULL,  flight_id int NOT NULL, passenger_id int NOT NULL, flight_date date NOT NULL, seat VARCHAR(4) NOT NULL, luggage_small int NOT NULL, luggage_large int NOT NULL, PRIMARY KEY (id), CONSTRAINT FK_flightID FOREIGN KEY (flight_id) REFERENCES Flights(id), CONSTRAINT FK_passengerID FOREIGN KEY (passenger_id) REFERENCES Passengers(id)')

##
##
##### Flash Handling

class Flash():
    def error(message):
        flash(message, category='error')

    def success(message):
        flash(message, category='success')

    def warning(message):
        flash(message, category='warning')

    def info(message):
        flash(message, category='info')




##
##
##### Ticket Handling
##
##

class Ticket:
    def insertTicket(ticket_id, flight_id, passenger_id, flight_date, seat, luggage_small, luggage_large):
        cursor.execute("INSERT INTO Tickets (ticket_id, flight_id, passenger_id, flight_date, seat, luggage_small, luggage_large) VALUES (%s, %s, %s, %s, %s, %s, %s)", (ticket_id, flight_id, passenger_id, flight_date, seat, luggage_small, luggage_large))
        db.commit()
        print(cursor.rowcount, " Ticket record inserted.")

    def getTicket(id):
        cursor.execute("SELECT * FROM Tickets WHERE id = %s", (id,))
        
        return cursor.fetchall()

    def getTickets():
        cursor.execute("SELECT * FROM Tickets")
        
        return cursor.fetchall()
    
    def deleteTicket(id):
        cursor.execute("DELETE FROM Tickets WHERE id = %s", (id,))
        db.commit()
        print(cursor.rowcount, " Ticket record deleted.")
    
    def getTickets_byUserID():
        userID = session.get('userID')
        passengers = Passenger.getPassengers_byUserID(userID)
        info = []
        for passenger in passengers:
            info.append(curser.execute("SELECT * FROM Tickets WHERE passenger_id = %s", (passenger[0],)))
        
        print(info)
        return info






##
##
#####  Passenger Handling
##
##

class Passenger:

    def insertPassenger(user_id, first_name, last_name, date_of_birth, gender, passport_number):

        if gender == 1:
            gender = "Male"
        elif gender == 2:
            gender = "female"
        else:
            gender = "Other"

        cursor.execute("INSERT INTO Passengers (user_id, first_name, last_name, date_of_birth, gender, passport_number) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, first_name, last_name, date_of_birth, gender, passport_number))
        db.commit()
        print(cursor.rowcount, " Passenger record inserted.")

    def getPassenger(id):
        cursor.execute("SELECT * FROM Passengers WHERE id = %s", (id,))
        return cursor.fetchall()

    def getPassengers():
        cursor.execute("SELECT * FROM Passengers")
        
        return cursor.fetchall()

    def getPassengers_byUserID():
        userID = session.get('userID')
        cursor.execute("SELECT * FROM Passengers WHERE user_id = %s", (userID,))
        
        return cursor.fetchall()

    def getPassengerByUIDandPID(passengerID):
        userID = session.get('userID')
        print(userID)
        print(passengerID)
        cursor.execute("SELECT * FROM Passengers WHERE user_id = %s AND id = %s", (userID, passengerID))
        
        return cursor.fetchone()
    
    def deletePassenger(id):
        cursor.execute("DELETE FROM Passengers WHERE id = %s", (id,))
        db.commit()
        print(cursor.rowcount, " Passenger record deleted.")

    def getPassenger_User_FirstName():
        id = session.get('userID')
        cursor.execute("SELECT id, first_name FROM Passengers WHERE user_id = %s", (id,))
        return cursor.fetchall()
    





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
        
        return cursor.fetchall()


        ## Returns a single flight with the given id
    def getFlight(id):
        cursor.execute("SELECT * FROM Flights WHERE id = %s", (id,))
        return cursor.fetchall()


        ## Returns an array of flights with the given departure and destination
    def getFlightFromTo(departure, destination):
        cursor.execute("SELECT * FROM Flights WHERE departure = %s AND destination = %s", (departure, destination))
        
        
        return cursor.fetchall()


        ## Returns an array of flights with the given departure
    def getFlightFrom(departure):
        cursor.execute("SELECT * FROM Flights WHERE departure = %s", (departure,))
        
        return cursor.fetchall()


        ## Returns an array of flights with the given destination
    def getFlightTo(destination):
        cursor.execute("SELECT * FROM Flights WHERE destination = %s", (destination,))
        
        return cursor.fetchall()


        ## Deleted a flight with the given id
    def deleteFlight(id):
        cursor.execute("DELETE FROM Flights WHERE id = %s", (id,))
        db.commit()
        print(cursor.rowcount, " Flight record deleted.")

    def getFlight_Distinct_Depart():
        cursor.execute("SELECT DISTINCT departure  FROM Flights ORDER BY departure ASC")
        
        return cursor.fetchall()

    def getFlight_Distinct_Dest():
        cursor.execute("SELECT DISTINCT destination  FROM Flights ORDER BY destination ASC")
        
        return cursor.fetchall()





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
        
        return cursor.fetchall()

    def getUserRecord_byEmail(email):
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        
        return cursor.fetchall()

    def getAllUsers():
        cursor.execute("SELECT * FROM Users")
        return cursor.fetchall()

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

    def emailExists():
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
    
    def phoneExists():
        cursor.execute("SELECT * FROM Users WHERE phone = %s", (phone,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False


    #cursor.execute("SELECT * FROM Users")
    #cursor.execute("DESCRIBE Users")

    #for x in cursor:
    #    print(x)

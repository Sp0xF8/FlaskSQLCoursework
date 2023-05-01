import mysql.connector as sql
from datetime import datetime, timedelta

from flask import flash, session

from werkzeug.security import generate_password_hash, check_password_hash

admins = [1]


db = sql.connect(
    host = "localhost",
    user =  "root",
    passwd = "AppleJack20",
    database = "horizonTravels"
)

cursor = db.cursor()

def WorkOutPrice(flight_id, ticket_type, days_before_flight):

    cursor.execute("SELECT * FROM Flights WHERE id = %s", (flight_id,))
    flight = cursor.fetchall()
    price = flight[0][5]

    if ticket_type == 2:
        price *= 2


    if (days_before_flight <= 90 and days_before_flight >= 80):
        price *= 0.8

    elif (days_before_flight < 80 and days_before_flight >= 60):
        price *= 0.9

    elif (days_before_flight < 60 and days_before_flight >= 45):
        price *= 0.95

    return price



class HelperFunctions:

    def PriceHelper(data):
        total_sales = 0

        for info in data:
            days_before_flight = info[3] - info[6]
            days_before_flight = days_before_flight.days
            total_sales += WorkOutPrice(info[2], info[4], days_before_flight)

        return total_sales

    
        

##
##
#####   Flash Handling
##
##

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
#####   Ticket Handling
##
##

class Ticket:
    def insertTicket(data):
        for each in data:

            passenger_id = each.get('passenger_id')
            flight_id = each.get('flight_id')
            flight_date = each.get('flight_date')
            luggage_type = each.get('luggageType')
            ticket_type = each.get('ticketType')
            purchase_date = (str)(datetime.now().strftime('%Y-%m-%d'))
            
            cursor.execute("INSERT INTO Tickets (passenger_id, flight_id, flight_date, ticket_type, luggage_type, purchase_date) VALUES (%s, %s, %s, %s, %s, %s)", (passenger_id, flight_id, flight_date, ticket_type, luggage_type, purchase_date))
            db.commit()
            

    def getTicket(id):

        cursor.execute("SELECT * FROM Tickets WHERE id = %s", (id,))
        return cursor.fetchall()

    def getTickets():

        cursor.execute("SELECT * FROM Tickets")
        return cursor.fetchall()
    
    def deleteTicket(id):

        cursor.execute("DELETE FROM Tickets WHERE id = %s", (id,))
        db.commit()
    
    def getTickets_byUserID():

        passengers = Passenger.getPassengers_byUserID()
        info = []

        for passenger in passengers:
            cursor.execute("SELECT * FROM Tickets WHERE passenger_id = %s", (passenger[0],))
            temp = cursor.fetchall()

            if len(temp) > 1:
                for each in temp:
                    info.append(each)

            elif len(temp) == 0:
                pass

            else:
                info.append(temp[0])

        return info

    def getTickets_Left_ByDate(flight_date, flight_id):
        
        cursor.execute("SELECT * FROM Tickets WHERE flight_date = %s AND flight_id = %s", (flight_date, flight_id))
        
        temp = cursor.fetchall()

        return len(temp)

    def getTickets_byFlightID(flight_id):
            
            cursor.execute("SELECT * FROM Tickets WHERE flight_id = %s", (flight_id,))
            return cursor.fetchall()
    
    def getMonthlySales():

        #get current date 30 days ago in yyy-mm-dd format
        mongth_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        


        cursor.execute("SELECT * FROM Tickets WHERE purchase_date BETWEEN %s AND %s", (mongth_ago, datetime.now().strftime('%Y-%m-%d')))
        temp = cursor.fetchall()
        
        
        return HelperFunctions.PriceHelper(temp)

    
    def bestCustomer():
        cursor.execute("SELECT u.*, COUNT(t.passenger_id) AS num_tickets FROM Users u JOIN Passengers p ON u.id = p.user_id JOIN Tickets t ON p.id = t.passenger_id GROUP BY u.id ORDER BY num_tickets DESC LIMIT 3;")
        
        temp = cursor.fetchall()
        result = []

        for each in temp:
            result.append([each[0], each[1], each[2], each[3]])

        return result
    
   
        

   

            
            

##
##
#####   Passenger Handling
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
        cursor.execute("SELECT * FROM Passengers WHERE user_id = %s AND id = %s", (userID, passengerID))

        return cursor.fetchone()
    
    def deletePassenger(id):

        cursor.execute("DELETE FROM Passengers WHERE id = %s", (id,))
        db.commit()

    def getPassenger_User_FirstName():

        id = session.get('userID')
        cursor.execute("SELECT id, first_name FROM Passengers WHERE user_id = %s", (id,))
        
        return cursor.fetchall()
    
    def getPassenger_byPassengerID(tickets):
        info = []

        for ticket in tickets:
            cursor.execute("SELECT * FROM Passengers WHERE id = %s", (ticket[1],))
            temp = cursor.fetchall()

            info.append(temp[0][2])

        return info

##
##
#####   FLIGHT HANDLING
##
##

class Flight:
        ## Create a new flight schedule
    def insertFlight(departure1, destination1, departure_time1, arrival_time1, price1):
        cursor.execute("INSERT INTO Flights (departure, destination, departure_time, arrival_time, price) VALUES (%s, %s, %s, %s, %s)", (departure1, destination1, departure_time1, arrival_time1, price1))
        db.commit()


        ## Returns an array of all flights
    def getFlights():
        cursor.execute("SELECT * FROM Flights")
        
        return cursor.fetchall()


        ## Returns a single flight with the given id
    def getFlight(id):
        cursor.execute("SELECT * FROM Flights WHERE id = %s", (id,))
        return cursor.fetchall()

    def getFlightbyIDforTicket(tickets):
        data = []
        
        for ticket in tickets:
            cursor.execute("SELECT * FROM Flights WHERE id = %s", (ticket[2],))
            temp = cursor.fetchall()
            data.append(temp[0])
    
        return data


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

    def getFlight_Distinct_Depart():
        cursor.execute("SELECT DISTINCT departure  FROM Flights ORDER BY departure ASC")
        
        return cursor.fetchall()

    def getFlight_Distinct_Dest():
        cursor.execute("SELECT DISTINCT destination  FROM Flights ORDER BY destination ASC")
        
        return cursor.fetchall()

##
##
#####   USER HANDLING
##
##

class User:

    def insertUser(first_name1, last_name1, email1, password1, DoB, phone1, address1, zip1):
        datenow = (str)(datetime.now().strftime('%Y-%m-%d'))

        date_of_birth1 = (str)(DoB.strftime('%Y-%m-%d'))



        password2 = generate_password_hash(password1, method='sha256')

        cursor.execute("INSERT INTO Users (first_name, last_name, email, password, date_of_birth , phone, address, zip, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (first_name1, last_name1, email1, password2, date_of_birth1, phone1, address1, zip1, datenow))
        db.commit()


    def dropUserRecord_byID(userID):
        cursor.execute("DELETE FROM Users WHERE id = %s", (userID,))
        db.commit()

    def dropUserRecord_byEmail(email):
        cursor.execute("DELETE FROM Users WHERE email = %s", (email,))
        db.commit()


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

    def updateUser(first_name, last_name, email, password, phone, address, zip_code):

        password2 = generate_password_hash(password, method='sha256')

        cursor.execute("UPDATE Users SET first_name = %s, last_name = %s, email = %s, password = %s, phone = %s, address = %s, zip = %s WHERE id = %s", (first_name, last_name, email, password2, phone, address, zip_code, session.get('userID')))
        db.commit()

    def updateUser_noPass(first_name, last_name, email, phone, address, zip_code):

        cursor.execute("UPDATE Users SET first_name = %s, last_name = %s, email = %s, phone = %s, address = %s, zip = %s WHERE id = %s", (first_name, last_name, email, phone, address, zip_code, session.get('userID')))
        db.commit()

    def loginHelperEmail(email):
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return user
        else:
            return False

    def getUser():
        if session.get('loggedin'):
            cursor.execute("SELECT * FROM Users WHERE id = %s", (session.get('userID'),))
            user = cursor.fetchone()
            return user
        else:
            return False

    def passCheck(password):
        cursor.execute("SELECT * FROM Users WHERE id = %s", (session.get('userID'),))
        user = cursor.fetchone()
        if user:
            if check_password_hash(user[4], password):
                return True
            else:
                return False
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
            temp = 0;
            for admin in admins:
                if session.get('userID') == admin:
                    temp = 1
                    break
            if temp == 0:
                return False
            else:
                return True
        else:
            return False

    def isLoggedin():
        if session.get('loggedin'):
            return True
        else:
            return False

    def emailExists(email):
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
    
    def phoneExists(phone):
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

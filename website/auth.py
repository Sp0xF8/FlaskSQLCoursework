from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from datetime import date


from .sqlHandeling import User, Flight, Passenger, Ticket

auth = Blueprint('auth', __name__)

# FIX LOGIN MODAL THING
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('floatingEmail')
        password = request.form.get('floatingPassword')

        if User.userLogin(email, password):
            return redirect(url_for('views.home'))

    return render_template("login.html")


@auth.route('/logout')
def logout():
    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))

    User.stopSession()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        age = request.form.get('signupBirth')
        DoB = date(int(age[0:4]), int(age[5:7]), int(age[8:10]))
        email = request.form.get('signupEmail')
        phone = request.form.get('signupPhone')
        address = request.form.get('signupAddress')
        zip_code = request.form.get('zip_code')
        password = request.form.get('signupPassword')
        passwordConfirm = request.form.get('signupPasswordConfirm')

        # Validation
        if len(firstName) < 3:
            flash('First name must be greater than 3 characters.', category='error')
        elif len(lastName) < 3:
            flash('Last name must be greater than 3 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif User.emailExists(email):
            flash('Email already exists.', category='error')
        elif len(phone) < 10:
            flash('Phone number must be greater than 10 characters.',
                  category='error')
        elif User.phoneExists(phone):
            flash('Phone number already exists.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        elif password != passwordConfirm:
            flash('Passwords do not match.', category='error')
        else:

            User.insertUser(firstName, lastName, email, password, DoB, phone, address, zip_code)



            User.userLogin(email, password)
            flash('Account created!', category='success')
            # Add user to database

            return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth.route('/admin', methods=['GET', 'POST'])
def admin():

    if(not User.isAdmin()):
        flash('You require greater permissions to access this page!', category='error')
        return redirect(url_for('views.restricted'))

    if request.method == 'POST':
        if (request.form.get('action') == 'deleteUser'):
            User.dropUserRecord_byID(request.form.get('userID'))
            flash('User deleted!', category='success')

        elif (request.form.get('action') == 'deleteFlight'):
            Flight.deleteFlight(request.form.get('flightID'))
            flash('Flight deleted!', category='success')

        elif (request.form.get('action') == 'createFlight'):
            Flight.insertFlight(request.form.get('departure'), request.form.get('destination'), request.form.get('departing'), request.form.get('arriving'), request.form.get('price'))
            flash('Flight added!', category='success')

    users = User.getAllUsers()

    flights = Flight.getFlights()

    return render_template("admin.html", userList=users, flightList=flights)


@auth.route('/bookings', methods=['GET', 'POST'])
def bookings():
    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))

    action = request.form.get('action')

    destination = request.form.get('destination')
    departure = request.form.get('departure')

    if request.method == 'POST':
        if (action == 'searchFlights'):
            if (destination and departure):
                flights = Flight.getFlightFromTo(departure, destination)

                if (flights):
                    
                    flash('Flights found!', category='success')
                    return render_template(
                        "bookings.html", 
                        passengerList=Passenger.getPassengers_byUserID(), 
                        flightList=Flight.getFlights(), 
                        flightDepartNames=Flight.getFlight_Distinct_Depart(), 
                        flightDestNames=Flight.getFlight_Distinct_Dest(),
                        departANDdest=flights
                        )

                else:
                    flash('No flights found!', category='error')

                    
            elif (destination and not departure):
                flights = Flight.getFlightTo(destination)

                if(flights):
                    flash('Flights found!', category='success')
                    return render_template(
                        "bookings.html", 
                        passengerList=Passenger.getPassengers_byUserID(), 
                        flightList=Flight.getFlights(), 
                        flightDepartNames=Flight.getFlight_Distinct_Depart(), 
                        flightDestNames=Flight.getFlight_Distinct_Dest(),
                        departANDdest=flights
                        )
                else:
                    flash(' No flights found!', category='error')

            elif(departure and not destination):
                flights = Flight.getFlightFrom(departure)
                if(flights):
                    flash('Flights found!', category='success')
                    return render_template(
                        "bookings.html", 
                        passengerList=Passenger.getPassengers_byUserID(), 
                        flightList=Flight.getFlights(), 
                        flightDepartNames=Flight.getFlight_Distinct_Depart(), 
                        flightDestNames=Flight.getFlight_Distinct_Dest(),
                        departANDdest=flights
                        )
                else:
                    flash('No flights found!', category='error')

            else:
                flash('Please select a destination and/or departure!', category='error')
        
        if (action == 'selectFlight'):


            return render_template(
                "bookings.html", 
                passengerList=Passenger.getPassengers_byUserID(), 
                flightList=Flight.getFlights(), 
                flightDepartNames=Flight.getFlight_Distinct_Depart(), 
                flightDestNames=Flight.getFlight_Distinct_Dest()
                )

    return render_template(
        "bookings.html", 
        passengerList=Passenger.getPassengers_byUserID(), 
        flightList=Flight.getFlights(), 
        flightDepartNames=Flight.getFlight_Distinct_Depart(), 
        flightDestNames=Flight.getFlight_Distinct_Dest()
        )


@auth.route('/passengers', methods=['GET', 'POST'])
def passengers():
    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))

    passengers = Passenger.getPassengers_byUserID()


    if request.method == 'POST':
        if (request.form.get('action') == 'deletePassenger'):
            Passenger.deletePassenger(request.form.get('passengerID'))
            flash('Passenger deleted!', category='success')
            
        elif (request.form.get('action') == 'createPassenger'):
            Passenger.insertPassenger(
                request.form.get('user_id'),
                request.form.get('first_name'), 
                request.form.get('last_name'), 
                request.form.get('date_of_birth'), 
                request.form.get('gender'),
                request.form.get('passport_number')
            )

            flash('Passenger added!', category='success')
        
           
    
    return render_template("passengers.html", passengerList=passengers)

@auth.route('/process', methods=['POST'])
def process():
    departure = None
    destination = None

    departure = request.form.get('departure')
    destination = request.form.get('destination')

    if ((destination == None) and (departure == None)):
        flash('Please select a Departure or Destination.', category='error')

    elif (destination == None):
        jsonify({'departure': departure})

    elif (departure == None):
        jsonify({'destination': destination})

    else:
        jsonify({'departure': departure},
                {'destination': destination})

        



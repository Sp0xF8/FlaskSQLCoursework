from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from datetime import date
from datetime import datetime


from .sqlHandeling import User, Flight, Passenger, Ticket, HelperFunctions
from .ajax import Ajax

auth = Blueprint('auth', __name__)


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
            return redirect(url_for('auth.login'))

    return render_template("register.html")

@auth.route('/edit_profile', methods=['POST'])
def edit_profile():
    
        if(not User.isLoggedin()):
            flash('You are not logged in.', category='error')
            return redirect(url_for('auth.login'))
    
        if request.method == 'POST':

            current_password = request.form.get('current_password')
            if (not User.passCheck(current_password)):
                flash('Current password is incorrect.', category='error')
                return "Incorrect password."
    
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address')
            zip_code = request.form.get('zip_code')

            if (request.form.get('confirm_password')):
                password = request.form.get('confirm_password')
                User.updateUser(first_name, last_name, email, password, phone, address, zip_code)
            else:
                User.updateUser_noPass(first_name, last_name, email, phone, address, zip_code)

            return "Account Updated!"
            
@auth.route('/profile', methods=['GET'])
def profile():

    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))

    return render_template("profile.html", 
            user=User.getUser())

@auth.route('/admin', methods=['GET', 'POST'])
def admin():

    if(not User.isAdmin()):
        flash('You require greater permissions to access this page!', category='error')
        return redirect(url_for('views.restricted'))

    

    if request.is_json:

        if request.method == 'GET':
            print("in json")    
            print(request.args.get('flight_id'))
            return Ajax.Tickets.getSales(request.args.get('flight_id'))

    

    if request.method == 'POST':

        if (request.form.get('action') == 'deleteUser'):
            User.dropUserRecord_byID(request.form.get('userID'))
            flash('User deleted!', category='success')
            return redirect(url_for('auth.admin'))

        elif (request.form.get('action') == 'deleteFlight'):
            Flight.deleteFlight(request.form.get('flightID'))
            flash('Flight deleted!', category='success')
            return redirect(url_for('auth.admin'))

        elif (request.form.get('action') == 'createFlight'):
            Flight.insertFlight(request.form.get('departure'), request.form.get('destination'), request.form.get('departing'), request.form.get('arriving'), request.form.get('price'))
            flash('Flight added!', category='success')
            return redirect(url_for('auth.admin'))

    users = User.getAllUsers()
    flights = Flight.getFlights()

    return render_template("admin.html", 
            userList=users, 
            flightList=flights,
            monthly_sales=Ticket.getMonthlySales(),
            best_customers=Ticket.bestCustomer())

@auth.route('/processPayment', methods=['GET', 'POST'])
def processPayment():

    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        data = request.get_json()
        Ticket.insertTicket(data)
        return "success"

@auth.route('/passengerDetails', methods=['GET', 'POST'])
def passengerDetails():

    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        passengerIDs = request.get_json()
        passengerValid = Ajax.Flight.getPassengerDetailsByID(passengerIDs)
        return jsonify(passengerValid)
   
@auth.route('/booking', methods=['GET', 'POST'])
def booking():

    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))

    flight = Flight.getFlight(id=request.args.get('flightID'))
    flight_date = request.args.get('flight_date')
    fixedList =[]

    totalTickets = Ticket.getTickets_Left_ByDate(flight_date, flight[0][0])

    innerTuple = flight[0]
    listConvert = list(innerTuple)
    listConvert[6] -= totalTickets
    
    if(listConvert[6] == 0):
        flash(message='No tickets left! Please try another date!', category='error')
        return redirect(url_for('auth.search'))

    fixedList.append(tuple(listConvert)) 

    passengers = Passenger.getPassengers_byUserID()

    return render_template("booking.html", 
            flight=fixedList, 
            flight_date=flight_date, 
            passengers=passengers)

@auth.route('/search', methods=['GET', 'POST'])
def search():

    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))


    if request.is_json:

        if request.method == 'GET':
            departure = request.args.get('departure')
            destination = request.args.get('destination')
            return jsonify(Ajax.Flight.search(departure, destination))
    
    return render_template(
            "search.html", 
            flightDepartNames=Flight.getFlight_Distinct_Depart(),
            flightDestNames=Flight.getFlight_Distinct_Dest()
            )

@auth.route('/passengers', methods=['GET', 'POST'])
def passengers():
    datenow = (str)(datetime.now().strftime('%Y-%m-%d'))

    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))

    passengers = Passenger.getPassengers_byUserID()

    if request.method == 'POST':

        if (request.form.get('action') == 'deletePassenger'):
            Passenger.deletePassenger(request.form.get('passengerID'))
            flash('Passenger deleted!', category='success')
            return redirect(url_for('auth.passengers'))
            
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
            return redirect(url_for('auth.passengers'))
        
    return render_template("passengers.html", passengerList=passengers, datenow=datenow)

@auth.route('/delete_ticket', methods=['GET', 'POST'])
def delete_ticket():
    
        if(not User.isLoggedin()):
            flash('You are not logged in.', category='error')
            return redirect(url_for('auth.login'))
    
        if request.method == 'POST':
            Ticket.deleteTicket(request.form.get('ticketID'))
            flash('Ticket deleted!', category='success')
    
        return redirect(url_for('auth.tickets'))

@auth.route('/tickets', methods=['GET', 'POST'])
def tickets():

    if(not User.isLoggedin()):
        flash('You are not logged in.', category='error')
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        tickets = Ticket.getTickets_byUserID()
        flightInfo = Flight.getFlightbyIDforTicket(tickets)
        length = len(tickets)
        first_names = Passenger.getPassenger_byPassengerID(tickets)

        return render_template("tickets.html", 
                ticketList=tickets, 
                flightInfo=flightInfo, 
                length=length, 
                first_names=first_names)

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

        



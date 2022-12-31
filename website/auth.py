from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import date


from .sqlHandeling import userLogin, insertUser, getUserRecord_byEmail, dropUserRecord_byID, loginHelperEmail, stopSession, getAllUsers

auth = Blueprint('auth', __name__)


# FIX LOGIN MODAL THING
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('floatingEmail')
        password = request.form.get('floatingPassword')

        if userLogin(email, password):
            return redirect(url_for('views.home'))

    return render_template("login.html")


@auth.route('/logout')
def logout():
    stopSession()
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
        elif len(phone) < 10:
            flash('Phone number must be greater than 10 characters.',
                  category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        elif password != passwordConfirm:
            flash('Passwords do not match.', category='error')
        else:

            insertUser(firstName, lastName, email, password, DoB, phone, address, zip_code)



            userLogin(email, password)
            flash('Account created!', category='success')
            # Add user to database

            return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth.route('/admin', methods=['GET', 'POST'])
def admin():

    users = getAllUsers()

    return render_template("admin.html", userList=users)

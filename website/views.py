from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('/bookings')
def bookings():
    return render_template("bookings.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

@views.route('/faq')
def faq():
    return render_template("faq.html")

@views.route('/gallery')
def gallery():
    return render_template("gallery.html")

@views.route('/privacy')
def privacy():
    return render_template("privacy.html")

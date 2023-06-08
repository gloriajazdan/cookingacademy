from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import  login_required, current_user
from .models import Classes
from . import db
from . import os
from datetime import date, datetime, time



mainbp = Blueprint('main', __name__)

#Index Page
@mainbp.route('/')
def index():
    classes=Classes.query.all()
    return render_template ('index.html', events=classes)

    
#User History Page
@mainbp.route('/myaccount')
@login_required
def userHistory():
    current_date = date.today()
    current_time = datetime.now().time()
    bookings = current_user.bookings
    current_bookings = []
    past_bookings = []

    for booking in bookings:
        if booking.booked_class.date < current_date:
            past_bookings.append(booking)
        elif booking.booked_class.date == current_date:
            if booking.booked_class.time < current_time:
                past_bookings.append(booking)
            elif booking.booked_class.time > current_time:
                current_bookings.append(booking)
        elif booking.booked_class.date > current_date:
            current_bookings.append(booking)
    

    return render_template('AccountPage.html', myBookings= current_bookings, pastBookings = past_bookings, myClasses= current_user.created_classes)


#FAQ Page
@mainbp.route('/FAQ.html')
def questions():
    return render_template('FAQ.html')

from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from .forms import BookingForm, EditClassForm, ClassForm, CommentForm
from flask_login import current_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from .models import Comments, Classes, Tickets
from . import db
from . import os

classes_bp = Blueprint('classes', __name__, url_prefix='/classes')

#Create Event
@classes_bp.route('/createclass', methods = ['GET', 'POST'])
@login_required
def eventCreation():
    cookingClass= ClassForm()
    if cookingClass.validate_on_submit():
        db_file_path=check_upload_file(cookingClass)
        new_class= Classes (title=cookingClass.title.data,
                            no_of_tickets=cookingClass.ticketsAvailable.data, 
                            cuisine=cookingClass.cuisine.data,
                            level=cookingClass.level.data, 
                            description=cookingClass.description.data, 
                            image=db_file_path, 
                            time=cookingClass.time.data, 
                            date=cookingClass.date.data, 
                            venue=cookingClass.venue.data,
                            status="Open",
                            price=cookingClass.price.data,
                            user_id=current_user.id)
        db.session.add(new_class)
        db.session.commit()
        flash("Class created successfully", "success")
        return redirect(url_for('main.index'))
    else:
        return render_template('EventCreation.html', form=cookingClass, heading="Create Event")
        
    
@classes_bp.route('/<id>')
def show(id):
    event = Classes.query.filter_by(id=id).first()
    # create the comment form
    comments_form = CommentForm()
    booking_form = BookingForm()
    if booking_form.validate_on_submit():
        return redirect(url_for('main.index'))
    return render_template('EventDetails.html', event=event, form=comments_form, booking_form=booking_form)


@classes_bp.route('/view_all')
def view_all_events():
    # perform search if available
    for arg in request.args:
        if (arg == 'q' and request.args['q'] != ''):
            searchQuery = request.args['q']
            events = Classes.query.where(Classes.title.contains(searchQuery) | Classes.description.contains(searchQuery)).all()
            return render_template('ClassSearch.html', heading='All Events', events=events)

    # get all active events
    events = Classes.query.filter(Classes.status != 'Inactive').all()            
    return render_template('ClassSearch.html', heading='All Events', events=events)


@classes_bp.route('/view_all/<genre>')
def view_events(genre):
    genre = genre.capitalize()
    genre_events_list = Classes.query.filter_by(cuisine=genre).filter(
        Classes.status != 'Inactive').all()
    return render_template('ClassSearch.html', genre=genre, events=genre_events_list)

@classes_bp.route('/<id>/update', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = Classes.query.get(id)
    # Provide the old event information in the form fields
    form = EditClassForm(
        cuisine=event.cuisine,
        title=event.title,
        venue=event.venue,
        time=event.time,
        date=event.date,
        description=event.description,
        ticketsAvailable=event.no_of_tickets,
        price=event.price,
        level= event.level)
    
    #check the current user is editing
    if current_user.id != event.user_id:
        flash("You can only edit your own events!", 'danger')
        return redirect(url_for('main.my_events'))
    if form.validate_on_submit():
        if (form.image.data is not None):
            # call the function that checks and returns image
            db_file_path = check_upload_file(form)
            Classes.query.filter_by(id=id).update(
                {'image': db_file_path}, synchronize_session='evaluate')
        Classes.query.filter_by(id=id).update(
            {'title': form.title.data, 'date': form.date.data, 'time': form.time.data,
             'venue': form.venue.data, 'description': form.description.data,
             'no_of_tickets': form.ticketsAvailable.data,
             'level': form.level.data,
             'price': form.price.data,
             'cuisine':  form.cuisine.data.capitalize()
            }, synchronize_session='evaluate')
        # commit to the database
        db.session.commit()
        flash('Successfully updated event!', 'success')
        # end with redirect when form is valid
        return redirect(url_for('main.userHistory'))
    return render_template('EventEdit.html', form=form, event=event, heading='Edit Event')


# Function to check if a booking should be allowed to execute
def check_tickets(form, event):
    
    if event.tickets_remaining  is None:
        flash("No more tickets avaiable!", 'warning')
        return False
    if form.data['ticket_num'] <= 0:
        flash("You must book at least one ticket!", 'warning')
        return False
    elif event.status == 'Cancelled' or event.status == 'Inactive':
        flash("Sorry, the event is not open for bookings.", 'danger')
        return False
    elif event.tickets_remaining - form.data['ticket_num'] < 0:
        flash("Your order cannot be placed as it exceeds the number of tickets remaining. Reduce the quantity and try again.", 'danger')
        return False
    # Otherwise let the booking go ahead
    else:
        # If this booking exhausts the remaining tickets, set it to Booked Out
        if event.tickets_remaining - form.data['ticket_num'] == 0:
            event.status = "Sold Out"
            return True
    return True

@classes_bp.route('/<id>/book', methods=['GET','POST'])
@login_required
def book_class (id):
    form = BookingForm()
    event = Classes.query.filter_by(id=id).first()
    #Tickets remaining is null before first purchase
    if (event.tickets_remaining == None):
        Classes.query.filter_by(id=event.id).update({'tickets_remaining': event.no_of_tickets - event.tickets_booked})
        db.session.commit()
        event = Classes.query.filter_by(id=id).first()
    if check_tickets(form, event):
        if form.validate_on_submit():
            new_tickets = Tickets(quantity=form.ticket_num.data, booking_date=datetime.now(), class_id = id, user_id = current_user.id)

            Classes.query.filter_by(id=id).update(
                {'tickets_booked': event.tickets_booked + form.ticket_num.data, 'tickets_remaining': event.no_of_tickets - event.tickets_booked - form.ticket_num.data } , synchronize_session = 'evaluate'
            )
            db.session.add(new_tickets)
            db.session.commit()
            flash_string = "You have taken the first step towards Yummy food. Your booking reference is: {}".format(
                 new_tickets.id)
            flash(flash_string,'success')
            return redirect(url_for('classes.show', id=id))
    return redirect(url_for('classes.show', id=id))



@classes_bp.route('/<id>/cancel', methods=['GET','POST'])
@login_required
def cancel_class(id):
    event = Classes.query.filter_by(id=id).first()
    if current_user.id != event.user_id:
        flash("You can only cancel your own events!", 'danger')
        return redirect(url_for('main.userHistory'))

    Classes.query.filter_by(id=id).update({'status': 'Cancelled'})
    db.session.commit()
    flash("Your class has been cancelled, you can undo this change from you My Account > My Classes screen", 'success')
    return redirect(url_for('classes.show', id=id))

@classes_bp.route('/<id>/reinstate', methods=['GET','POST'])
@login_required
def reinstate(id):
    event = Classes.query.filter_by(id=id).first()
    if current_user.id != event.user_id:
        flash("You can only reinstate your own events!", 'danger')
        return redirect(url_for('main.userHistory'))

    if event.tickets_remaining == 0:
        Classes.query.filter_by(id=id).update({'status': 'Sold Out'})
    else:    
        Classes.query.filter_by(id=id).update({'status': 'Open'})
    db.session.commit()
    flash("Your class has been reinstated", 'success')
    return redirect(url_for('classes.show', id=id))


#Comment
@classes_bp.route('/<id>/comment', methods=['GET','POST'])
@login_required
def Comment(id):
    form = CommentForm()
    event_obj = Comments.query.filter_by(id = id).first()
    if form.validate_on_submit():
        comment = Comments(text=form.text.data, 
                            class_id=id,
                            user_id = current_user.id)
        db.session.add(comment)
        db.session.commit()
        print("Comment Submitted")
    return redirect(url_for('classes.show', id =id))


#Check File
def check_upload_file(form):  
  fp=form.image.data
  filename=fp.filename
  BASE_PATH=os.path.dirname(__file__)
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  db_upload_path='/static/image/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path
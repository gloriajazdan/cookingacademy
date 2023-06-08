from flask import Flask
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DecimalField, RadioField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, DataRequired, Regexp
from flask_wtf.file import FileAllowed, FileRequired, FileField

ALLOWED_FILE={'png', 'PNG', 'jpg', 'JPG', 'JPEG', 'jpeg'}

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("Username:", validators=[
        InputRequired("Enter your registered username...")])
    password=PasswordField("Password:", validators=[
        InputRequired("Enter the password associated with you registered username...")])
    submit=SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("Username:", validators=[
        InputRequired("You must provide a unique username"),
        Length(min=5, max=30, message="Your username can only be between 5 and 30 characters ")])
    email=StringField("Email Address:", validators=[
        Email("You must provide a valid email address")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm=PasswordField("Re-enter your password to confirm")
    #To ensure the phone number provided by the user includes a '0' at the beginning and consists of a total of 10 digits.
    mobile=StringField('Mobile Number', validators=[
        DataRequired(), Regexp(r'^0\d{9}$', message='Invalid phone number. Must start with 0 and have a total of 10 digits.')])
    address=StringField("Home Address:", validators=[InputRequired('You must provide your home address to finish your registeration'
                                                                   )])
    #submit button
    submit = SubmitField("Create an Account!")
    
    # Creating Cooking Classes form:
class ClassForm (FlaskForm):
    
    title=StringField("The Title of the Class:", validators=[
        InputRequired("You must provide a title for the class"),
        Length(min=5, max=30, message="Class Title can only be between 5 and 30 characters")])
    description=TextAreaField("A Description of the Class:", validators=[
        InputRequired("You must provide a description for the class"),
        Length(max=500, message="The Class Description cannot exceed 500 characters")])
    cuisine=StringField("The Cuisine of the Class:", validators=[
        InputRequired("You must provide a cuisine of the class")])
    level= RadioField('The Difficulty Level of the Class:', choices=[('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')], validators=[
        InputRequired("You must select the level of the class")])
    venue=StringField("The Venue of the Class:", validators=[
        InputRequired("You must provide a venue where the class will be held")])
    date=DateField("The Date of the Class:", validators=[
        InputRequired(message="You must provide the Date of the class")])
    time=TimeField("The Time of the Class:", validators=[
        DataRequired(message="You must provide the Time of the class")])
    
    image=FileField("A Photo that Describes Your Class:", validators=[
        FileRequired(message = "An Image must be provided"), 
        FileAllowed(ALLOWED_FILE, message="Only supports png, jpg, PNG or JPG")])
    price=DecimalField("The Price Per Ticket:",validators=[
        InputRequired("You must provide the price per ticket in AUD")])
    ticketsAvailable=IntegerField('The Number of Tickets Available for Sale:', validators=[
        NumberRange(min=1, max=1000, message="The number of tickets must be at least 1 and at most 1000"),
        InputRequired("You must enter the number of tickets available for this class") ])
    submit=SubmitField("Create a Class!")

#Form for Editing the Classes 

class EditClassForm(FlaskForm):
    title=StringField("The title of the class", validators=[
        InputRequired("You must provide a title for the class"),
        Length(min=5, max=30, message="Class Title can only be between 5 and 30 characters")])
    description=TextAreaField("A description of the class", validators=[
        InputRequired("You must provide a description for the class"),
        Length(max=500, message="The Class Description cannot exceed 500 characters")])
    cuisine=StringField("The cuisine of the class", validators=[
        InputRequired("You must provide a cuisine of the class")])
    level= RadioField('The Difficulty Level of the Class:', choices=[('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')], validators=[
        InputRequired("You must select the level of the class")])
    venue=StringField("The venue of the class", validators=[
        InputRequired("You must provide a venue where the class will be held")])
    date=DateField("The date of the class", validators=[
        InputRequired(message="You must provide the Date of the class")])
    time=TimeField("The time of the class", validators=[
        DataRequired(message="You must provide the Time of the class")])
    
    image=FileField("Class Image", validators=[
        FileAllowed(ALLOWED_FILE, message="Only supports png, jpg, PNG or JPG")])
    price=DecimalField("The price per ticket",validators=[
        InputRequired("You must provide the price per ticket in AUD")])
    ticketsAvailable=IntegerField('The number of tickets available for sale', validators=[
        NumberRange(min=1, max=1000, message="The number of tickets must be at least 1 and at most 1000"),
        InputRequired("You must enter the number of tickets available for this class") ])
    submit=SubmitField("Confirm changes")
    
    
   #Booking
class BookingForm(FlaskForm):
    ticket_num=IntegerField("How many tickets are you purchasing?", default="1", validators=[InputRequired("You must enter the required number of tickets")])
    
    purchase = SubmitField("Purchase Tickets!")

        
    # Creates a comment form:
class CommentForm (FlaskForm):
    text=TextAreaField("Enter your comment here...", [InputRequired("You must enter your comment in the provided text area"), 
                                                      Length(max=1000, message="Your comment cannot exceed 1000 characters")])
    submit=SubmitField("Add your comment")

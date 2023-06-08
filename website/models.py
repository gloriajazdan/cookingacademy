from flask_login import UserMixin
from . import db
from datetime import datetime

# Users Table
class User (db.Model, UserMixin):
    __tablename__='users'
    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String (80), index=True, unique=True, nullable=False)
    emailid= db.Column(db.String(50), nullable=False)
    password_hash=db.Column(db.String(255), nullable=False)
    phone_number=db.Column(db.String(10), nullable=False)
    #address need to be added as per the task sheet, Part 1 Project Requirements, Point 8
    address=db.Column(db.String(200), nullable=False)
    #Linking the relationships with other tables 
    comments = db.relationship('Comments', backref='user')
    created_classes = db.relationship('Classes', backref='user', order_by="Classes.date.desc()")
    bookings = db.relationship('Tickets', backref='user')

    def __repr__(self):
         return "<Name: {}>".format(self.username)   
    
    
#Classes Table
class Classes (db.Model):
    __tablename__='classes'
    id=db.Column(db.Integer, primary_key=True)
    cuisine=db.Column(db.String(20), index=True, nullable=False)
    status=db.Column(db.String(20), index=True, nullable=False)
    title=db.Column(db.String(30), nullable=False) 
    level=db.Column(db.String(30), nullable=False)
    venue=db.Column(db.String(80), nullable=False)
    date=db.Column(db.Date, nullable=False)
    time=db.Column(db.Time, nullable=False)
    description=db.Column(db.String(500), nullable=False)
    image=db.Column(db.String(400), nullable=False)
    no_of_tickets=db.Column(db.Integer, nullable=False)
    tickets_booked= db.Column(db.Integer, default=0, nullable=False)
    tickets_remaining = db.Column(db.Integer)
    price=db.Column(db.Float, nullable=False)

    #Relationships and Foreign Keys
    
    comments = db.relationship('Comments', backref='class')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key column

    
    def __repr__(self):
        return "<Class Title: {}>".format(self.title)
    

   
#Tickets Table
class Tickets(db.Model):
    __tablename__='tickets'
    id=db.Column(db.Integer, primary_key=True)
    booking_date=db.Column(db.DateTime, default=datetime.now)
    quantity=db.Column(db.Integer, nullable=False)
    booked_class = db.relationship('Classes', backref='tickets')
    #Link relationships and add foreigh keys
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
         return "<Name: {}, id: {}>".format(self.title, self.id)
    
#Comments Table
class Comments(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now)
    #Foreign Keys
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __repr__(self):
        return "<Comment: {} By {}>".format(self.text, self.user_id)



    
    
    
    
    
    

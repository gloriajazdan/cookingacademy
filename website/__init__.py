from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import datetime, date, time

import threading 

db=SQLAlchemy()

#create a function that creates a web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=False
    app.secret_key='randomsecretvalue'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///cookingacademydb.sqlite'
    
    #initialise db with flask app
    db.init_app(app)

    bootstrap = Bootstrap5(app)
    
    #Create the images upload file path
    UPLOAD_FOLDER = '/static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
     #create a user loader function takes userid and returns User
    @login_manager.user_loader
    def load_user(user_id):
      from .models import User
      return User.query.get(int(user_id))
    
    #Update Class Status to Inactive:
    def check_class_status():
      with app.app_context():
        from .models import Classes 
        classes=Classes.query.filter(Classes.status != 'Inactive').all()
        current_day = date.today()
        current_time = datetime.now().time()
        for event in classes:
          if event.date < current_day:
            Classes.query.filter_by(id = event.id).update({'status' : "Inactive"})
            db.session.commit()
          elif event.date == current_day:
            if event.time < current_time:
              Classes.query.filter_by(id = event.id).update({'status' : "Inactive"})
              db.session.commit()
            
              
              #Schedule the task to run automatically
        threading.Timer(3600, check_class_status).start()
    
    check_class_status()
   
    #importing views module here to avoid circular references
    from . import views
    app.register_blueprint(views.mainbp)

    from . import auth, classes
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(classes.classes_bp)
    
    #Error 404
    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter
    def not_found(e): 
      return render_template("404.html")

    #Error 500
    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('500.html'), 500

#code to get the dynamic content for index page.
    @app.context_processor
    def get_context():
      from website.models import Classes
      all_classes = Classes.query.all()
      # On launch, check if there are any events that are now in the past
      # and if so, change them to Inactive
      for event in all_classes:
          if event.date < date.today():
              event.event_status='Inactive'
      current_events = Classes.query.filter(Classes.status!='Inactive').order_by(Classes.date).limit(4).all()
      db.session.commit()
      
      return(dict(events_list=all_classes,current_events=current_events))

    
    return app





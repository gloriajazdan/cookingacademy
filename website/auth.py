from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db

#create a blueprint
auth_bp = Blueprint('auth', __name__)

#Login function
@auth_bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    print('In Login View function')
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = User.query.filter_by(username=user_name).first()
        if user is None:
            error='Incorrect credentials supplied'
        elif not check_password_hash(user.password_hash, password): # takes the hash and password
            error='Incorrect credentials supplied'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') #this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None:
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

#Registration
@auth_bp.route('/register', methods=['GET','POST'])
def register():
    register = RegisterForm()
    if (register.validate_on_submit() == True):
            user_name = register.user_name.data
            pwd = register.password.data
            email=register.email.data
            Phone_Number=register.mobile.data
            Address=register.address.data
            u1 = User.query.filter_by(username = user_name).first()
            if u1:
                flash('User name already exists')
                return redirect(url_for('auth.login'))
            pwd_hash = generate_password_hash(pwd)
            new_user = User(username = user_name,   
                            password_hash=pwd_hash,     
                            emailid=email,  
                            phone_number=Phone_Number,  
                            address = Address)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    else:
        return render_template('user.html', form=register, heading='Register')


#Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from app import app, db, bcrypt
from app.forms import RegistrationForm,LoginForm,UploadForm
from app.models import User
from flask_login import login_user,current_user,logout_user,login_required
import os
from werkzeug import secure_filename
from flask_login import login_user,current_user,logout_user
import nexmo
import datetime
import random


# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
UPLOAD_FOLDER = os.path.basename('./uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TESTING']=False

client=nexmo.Client(key='d6ab2286', secret='2StTxLOOxYq5OaxF')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,fname=form.fname.data,lname=form.lname.data,weight=form.weight.data,height=form.height.data,mobile=form.mobile.data,email=form.email.data,password=hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully {form.username.data}!', 'success')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/uploadform",methods=['GET','POST'])
def uploadform():
    form=UploadForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('uploadform.html', title='UploadForm', form=form)

        





@app.route("/forgotpassword",methods=['GET','POST'])
def index():
    form=ForgotForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        # number="91"+str(user.mobile)
        number='919833760985'
        Message=str(random.randint(100000,999999))
        hashed_password = bcrypt.generate_password_hash(Message).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        response=client.send_message({'from': 'Nexmo', 'to':number,'text':'Your temporary password is '+Message})

        return redirect(url_for('login'))
    else:
         print(form.errors)
    return render_template('forgot.html',title='Message',form=form)


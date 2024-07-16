import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from chatapp.forms import registrationForm, loginForm
from chatapp.models import User
from chatapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required





# Route for user registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Username already exists. Please use a different Username.', 'error')
            return redirect(url_for('register'))
        if existing_email:
            flash('Email address already exists. Please use a different email.', 'error')
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash(f'Account succesfully created for {form.username.data}, now you can log in!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


# Route for user login
@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Loggged in succesfully' , 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Log in attempt Unsuccesfully' , 'error')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


# Route for user logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))




# Route for the home page
@app.route("/")
def index():
    return render_template("home.html")

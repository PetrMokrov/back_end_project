from flask import render_template, flash, redirect, url_for, request
from web_app import app
from web_app.forms import LoginForm, RegistrationForm
from web_app.models import User
from web_app import USM
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from web_app.tokens import generate_confirmation_token, confirm_token
from web_app import email_sender
from web_app import login_manager
import json

@app.route('/')
@app.route('/index')
@login_required
def index():
    if not current_user.is_confirmed():
        flash('Uups, you have not confirmed your email.')
        return redirect(url_for('login'))

    posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Portland!',
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!',
                'image': 'http://redcapes.it/wp-content/uploads/2018/04/Avengers-Infinity-War-official-poster-1.jpg'
            },
            {
                'author': {'username': 'Peter'},
                'body': 'The raccoon is still counting our chances to pass this project!',
                'image': 'https://media.giphy.com/media/uJi32NRF7jOA8/giphy-downsized-large.gif'
            },
            ]
    return render_template('index.html', login=current_user.login, title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_confirmed():
            print("authenticated, confirmed")
            return redirect(url_for('index'))
        if not current_user.is_confirmed():
            token = generate_confirmation_token(current_user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            email_sender.send(json.dumps({"email": current_user.email, "token":confirm_url}))
            flash('To complete your registration, confirm your email')
            print("authenticated, not confirmed")
            logout_user()
            return redirect(url_for('login'))
    form = LoginForm()
    if form.validate_on_submit():
        user = USM.select(form.username.data, category='login')
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if user.confirmed:
            print("authenticated, confirmed after login")
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            print("authenticated, not confirmed after login")
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            email_sender.send(json.dumps({"email": user.email, "token":confirm_url}))
            flash('Uups, you have not confirmed your email.')
            logout_user()
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        USM.insert(user)
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        email_sender.send(json.dumps({"email": user.email, "token":confirm_url}))
        flash('To complete your registration, confirm your email')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/confirm/<token>')
#@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        print("not confirmed")
        flash('The confirmation link is invalid or has expired.')   
        return redirect(url_for('login'))
    user = USM.select(email, category='email')
    if user.confirmed:
        print("already confirmed")
        flash('Account already confirmed. Please login.')
        return redirect(url_for('login'))
    else:
        print("confirmed")
        flash('Account with email {} confirmed! Just login'.format(email))
        if USM.confirm(email, category='email'):
            test_usr = USM.select(email, category='email')
            if not test_usr.confirmed:
                assert( 1 == 0)
            return redirect(url_for('login'))
        else:
            assert(1 == 2)

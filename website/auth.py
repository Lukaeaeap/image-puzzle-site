from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)

LANGUAGE = "en"

with open(f"website/static/languages/{LANGUAGE}.json", "r") as f:
    textlg = json.load(f)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        creation_date = request.form.get('creation_date')

        user = User.query.filter_by(email=email).first()
        user_check2 = User.query.filter_by(user_name=user_name).first()

        if user:
            flash(textlg['flashes']['email_exists'], category='error')
        elif user_check2:
            flash(textlg['flashes']['username_exists'], category='error')
        elif len(email) < 4:
            flash(textlg['flashes']['email_short'], category='error')
        elif len(first_name) < 2:
            flash(textlg['flashes']['firstname_short'], category='error')
        elif password1 != password2:
            flash(textlg['flashes']['password_no_match'], category='error')
        elif len(password1) < 7:
            flash(textlg['flashes']['password_short'], category='error')
        else:
            # Add the user to the database
            new_user = User(email=email, first_name=first_name, user_name=user_name, last_name=last_name,
                            password=generate_password_hash(password1, method='sha256'), creation_date=creation_date)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            # when logged in go back to the home page
            return redirect(url_for('views.home'))
    return render_template("register.html", user=current_user)


@auth.route('/login')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Filter the user for the email, and look at the first email (which is unique so there is only one).
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(textlg['flashes']['logged_in'], category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(textlg['flashes']['wrong_password'], category='error')
        else:
            flash(textlg['flashes']['no_match'], category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(textlg['flashes']['logged_out'], category='succes')
    return redirect(url_for('auth.login'))

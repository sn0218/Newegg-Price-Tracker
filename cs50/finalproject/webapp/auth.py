from flask import Blueprint, flash, redirect, url_for, render_template, request, session
from flask.helpers import url_for
from . import db, mail
from .models import Users
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
# import python regular expression to check if a string contains the specified search pattern
import re
from flask_mail import Message

auth = Blueprint('auth', __name__)


@auth.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        oldpw = request.form.get("oldpassword")
        newpw = request.form.get("newpassword")
        confirm = request.form.get("confirmation")

        # query the database for the username
        user = Users.query.filter_by(username=current_user.username).first()

        if not oldpw:
            flash("Missing Old Password.", category="error")
            return redirect(url_for("auth.edit"))
        elif not newpw:
            flash("Missing New Password.", category="error")
            return redirect(url_for("auth.edit"))
        elif not confirm:
            flash("Missing New Password Confirmation.", category="error")
            return redirect(url_for("auth.edit"))
        # ensure confirmation matches new password
        elif not newpw == confirm:
            flash("New Passwords don't match", category="error")
            return redirect(url_for("auth.edit"))
        # ensure the password is correct
        elif not check_password_hash(user.password, oldpw):
            flash("Incorrect password", category="error")
            return redirect(url_for("auth.login"))
        else:
            # hash new password and update the user password
            user.password = generate_password_hash(newpw, method='pbkdf2:sha256', salt_length=8)
            db.session.commit()

            flash(f"Password is changed successful!", category="success")

            return redirect("/")

    else:
        return render_template("editpw.html", user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register():
    
    # clear the login status while in registration
    logout_user()

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password") 
        password2 = request.form.get("confirmation")
        
        # query the database for the username
        user = Users.query.filter_by(username=username).first()

        # check the availability of username
        if user:
            flash("Username already exists.", category="error")
            return redirect(url_for("auth.register"))
        # ensure username is submitted
        elif not username:
            flash("Missing Username.", category="error")
            return redirect(url_for("auth.register"))
        # ensure password is submitted
        elif not password:
            flash("Missing Password.", category="error")
            return redirect(url_for("auth.register"))
        # ensure confirmation is submitted 
        elif not password2:
            flash("Missing Password Confirmation.", category="error")
            return redirect(url_for("auth.register"))
        # ensure the length of username
        elif len(username) < 6:
            flash("Invalid credential: Username must be at least 6 characters long.", category="error")
            return redirect(url_for("auth.register"))
        # ensure the length of password 
        elif len(password) < 7:
            flash("Invalid credential: Password must be at least 7 characters long.", category="error")
            return redirect(url_for("auth.register"))
        # ensure the validity of password 
        elif re.search(r"[A-Z]", password) is None:
            flash("Invalid credential: Password must contain at least one uppercase character.", category="error")
            return redirect(url_for("auth.register"))
        # ensure confirmation is matched to password
        elif not password == password2:
            flash("Invalid credential: Passwords don't match", category="error")
            return redirect(url_for("auth.register"))
        # ensure email is submitted and valid
        elif not email:
            flash("Missing Email", category="error")
            return redirect(url_for("auth.register"))     
        else:        
            # define the user and hash the password
            new_user = Users(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))           
            # insert the new user into database
            db.session.add(new_user)
            # commmit the database that change is made
            db.session.commit()

            # login_user and remeber the user after their sesssion expires
            login_user(new_user, remember=True)

            sendemail(email)

            flash(f"Registration successful!    Welcome, {username}", category="success")

            return redirect("/")

    else:  
        return render_template("register.html", user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password") 
        
        # query the database for the username
        user = Users.query.filter_by(username=username).first()

        # ensure username exist
        if not user:
            flash("Incorrect username", category="error")
            return redirect(url_for("auth.login"))
        # ensure the password is correct
        elif not check_password_hash(user.password, password):
            flash("Incorrect password", category="error")
            return redirect(url_for("auth.login"))
        else:
            login_user(user, remember=True)
            flash(f"Login successful!   Welcome, {username}", category="success")

            return redirect("/")
    else:
        return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login")) 


@auth.route("/clear")
@login_required
def clear():
    Users.query.delete()
    db.session.commit()
    return redirect(url_for("auth.login")) 

def sendemail(recipientemail):
    msg = Message(subject="Newegg Price Tracker Registration Successful",
    sender = 'samuelnhc@gmail.com',
                    recipients=[recipientemail], # replace with your email for testing
                    body="")
    mail.send(msg)
from flask import Flask, render_template, request, redirect, session, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Security: Session settings
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstcrud.db'
db = SQLAlchemy(app)

# CSRF Protection
csrf = CSRFProtect(app)

# Password hashing
bcrypt = Bcrypt(app)

# --------------------------
# 1. Secure Input Handling (Validation & Sanitization)
# --------------------------
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=3, max=20)])
    submit = SubmitField("Login")

class ContactForm(FlaskForm):
    fname = StringField("First Name", validators=[InputRequired(), Length(max=100)])
    lname = StringField("Last Name", validators=[InputRequired(), Length(max=100)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=100)])
    submit = SubmitField("Submit")

# --------------------------
# 2. Secure Password Storage (HASHING)
# --------------------------
# NOTE: Not used here since you hardcoded credentials. Replace with DB-based user model if needed.

USERNAME_HASH = bcrypt.generate_password_hash("kali").decode('utf-8')

# --------------------------
# Model
# --------------------------
class FirstApp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))

# --------------------------
# Routes
# --------------------------
@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == "kali" and bcrypt.check_password_hash(USERNAME_HASH, password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            return render_template("login.html", form=form, error="Invalid credentials")
    return render_template("login.html", form=form)

@app.route("/dashboard", methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect('/')
    form = ContactForm()
    if form.validate_on_submit():
        try:
            fname = re.sub(r"[^\w\s]", "", form.fname.data)
            lname = re.sub(r"[^\w\s]", "", form.lname.data)
            email = form.email.data.strip()
            entry = FirstApp(fname=fname, lname=lname, email=email)
            db.session.add(entry)
            db.session.commit()
            return redirect('/dashboard')  
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {e}", 500
    allrecord = FirstApp.query.all()
    return render_template('Index.html', allrecord=allrecord, form=form)


@app.route('/delete/<int:sno>')
def delete(sno):
    if 'user' not in session:
        return redirect('/')
    record = FirstApp.query.get_or_404(sno)
    db.session.delete(record)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if 'user' not in session:
        return redirect('/')
    record = FirstApp.query.get_or_404(sno)
    form = ContactForm(obj=record)
    if form.validate_on_submit():
        try:
            record.fname = re.sub(r"[^\w\s]", "", form.fname.data)
            record.lname = re.sub(r"[^\w\s]", "", form.lname.data)
            record.email = form.email.data.strip()
            db.session.commit()
            return redirect('/dashboard')  # Redirect after POST
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {e}", 500
    return render_template('update.html', form=form, record=record)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/')

# --------------------------
# 4. Secure Error Handling
# --------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)  

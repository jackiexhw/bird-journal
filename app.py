from tabnanny import check
from flask import Flask, render_template, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import datetime
from datetime import date

#init app
app = Flask(__name__)

# ENV = 'prod'
ENV = 'dev'
if ENV == 'dev':
    #development database
    app.debug = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dancingB1rB91@localhost/bird-journal'
else:
    #production database
    app.debug = False
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pgrvldbasmwkhz:7384bb689e34244b42a528cb4bb8e2e39519387adb7a7cf67607059ac40a8ab8@ec2-18-209-169-66.compute-1.amazonaws.com:5432/dd3ccj2st3h7ot'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#create database
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    # one to many rel with Entries table, can access entry's user with .user
    children = db.relationship('Entries')

    def __init__(self, username, password, creation_date=date.today()):
        self.username = username
        self.password = password
        self.creation_date = creation_date
        # self.children = children


class Entries(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100))
    loc = db.Column(db.String(100))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    notes = db.Column(db.Text())
    # image = db.Column()
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

    def __init__(self, species, loc, date, time, notes=None, image=None):
        self.species = species
        self.loc = loc
        self.date = date
        self.time = time
        self.notes = notes
        #self.image = image

# db.create_all()
# db.session.commit()

# create route for home page, decorator
@app.route('/')
def index():
    return render_template('login.html')
    return render_template('register.html')

@app.route('/success/', methods=['POST'])
def success():
    if request.method == 'POST':
        if request.form['success'] == "Back to Form":
            return render_template('index.html')
    
# submitting to /submit, array of allowed methods
@app.route('/submit/', methods=['POST'])
def submit():
    #make sure it's post request
    if request.method == 'POST':
        # assign form data to variables
        species = request.form['species']
        loc = request.form['loc']
        date = request.form['date']
        time = request.form['time']
        notes = request.form['notes']
        image = request.form['image']
        # print(species, loc, date, time, notes)
        if species == '' or loc == '' or date is None or time is None:
            return render_template('index.html', message="Incomplete form, please fill out all required fields.")
        data = Entries(species, loc, date, time, notes, image)
        db.session.add(data)
        db.session.commit()
        return render_template('success.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['lr_button'] == "Register":
            return render_template('register.html')
    # elif request.method == 'POST':
        elif request.form['lr_button'] == "Login":
            usr = request.form['username']
            pswd = request.form['password']
            if usr == '' or pswd == '':
                return render_template('login.html', message="Please enter a username and password.")
            else:
                db_users = db.engine.execute("SELECT * FROM users WHERE username='%s'" % usr)
                # if not db_users.all():
                #     flash("User does not exist")
                #     return render_template('login.html')
                # else:
                for user in db_users:
                    hashed_pw = user[2]
                    if check_password_hash(hashed_pw, pswd):
                        # flash("Login successful")
                        return render_template('index.html')
                    else:
                        return render_template('login.html', message="Username or password incorrect.")
    #TODO: message not displaying
    return render_template('login.html', message="Username or password incorrect.")

@app.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
        usr = request.form['username']
        pswd = request.form['password']
        if usr == '' or pswd == '':
            return render_template('register.html', message="Please enter a username and password.")
        else:
            # TODO: check if username already taken
            db_users = db.engine.execute("SELECT * FROM users WHERE username='%s'" % usr)
            for _ in db_users:
                flash('Username already taken, please try a different username.', 'error')
                return render_template('register.html')#, message='Username already taken, please try a different username.')
            pswd = generate_password_hash(pswd, method='sha256')
            user = Users(usr, pswd)#, creation_date)
            db.session.add(user)
            db.session.commit()
            return render_template('index.html')

#make sure it's running
if __name__ == '__main__':
    app.run()
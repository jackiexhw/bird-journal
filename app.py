from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime

#init app
app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    #development database
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dancingB1rB91@localhost/bird-journal'
else:
    #production database
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_DATABASE_URI'] = False
#create database
db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100))
    loc = db.Column(db.String(100))
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    year = db.Column(db.Integer)
    # date = datetime.date(year, month, day)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    # time = datetime.time(hour, minute)
    notes = db.Column(db.Text())
    # image = db.Column(db.String(100), unique=True)

    def __init__(self, species, loc, month, day, year, hour, minute, notes):
        self.species = species


# create route for home page, decorator
@app.route('/')
def index():
    return render_template('index.html')
    
# submitting to submit, array of allowed methods
@app.route('/submit', methods=['POST'])
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
        if species == '' or loc == '' or date == '' or time == '':
            return render_template('index.html', message="Incomplete form, please fill out all required fields.")
        return render_template('success.html')

#make sure it's running
if __name__ == '__main__':
    app.debug = True
    app.run()
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime

#init app
app = Flask(__name__)

ENV = 'prod'
if ENV == 'dev':
    #development database
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/bird-journal'
else:
    #production database
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pgrvldbasmwkhz:7384bb689e34244b42a528cb4bb8e2e39519387adb7a7cf67607059ac40a8ab8@ec2-18-209-169-66.compute-1.amazonaws.com:5432/dd3ccj2st3h7ot'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#create database
db = SQLAlchemy(app)

class Entries(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100))
    loc = db.Column(db.String(100))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    notes = db.Column(db.Text())
    # image = db.Column()

    def __init__(self, species, loc, date, time, notes=None, image=None):
        self.species = species
        self.loc = loc
        self.date = date
        self.time = time
        self.notes = notes
        #self.image = image



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
        if species == '' or loc == '' or date is None or time is None:
            return render_template('index.html', message="Incomplete form, please fill out all required fields.")
        data = Entries(species, locl date, time, note, image)
        db.session.add(data)
        db.session.commit()
        return render_template('success.html')

#make sure it's running
if __name__ == '__main__':
    app.run()
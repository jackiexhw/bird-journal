from flask import Flask, render_template, request

#init app
app = Flask(__name__)

#create route for home page, decorator
@app.route('/')
def index():
    return render_template('index.html')

#make sure it's running
if __name__ == '__main__':
    app.debug = True
    app.run()
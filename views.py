from flask import *
from main import app,db
#from models import items
#from forms import queryform, itemform

@app.route("/")
def login():
    return render_template('index.html')
import os
from flask import Flask
import sqlalchemy as db



app = Flask(__name__)
app.config['HOST'] = 'localhost'
app.config['PORT']=5003
app.config['DEBUG'] = True
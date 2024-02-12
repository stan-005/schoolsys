from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sys

app  = Flask(__name__)

app.config['SECRET_KEY']= '0f3991c35406b3dd6989'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nehecode@localhost:5432/school'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import schoolsys.views
import schoolsys.models


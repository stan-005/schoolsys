from datetime import datetime, timedelta
from schoolsys import db

class Students(db.Model):
    __tablename__ = "students"
    id          = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(100), unique=True, index=True)
    second_name = db.Column(db.String(100), unique=False, index=True)
    fee_paid    = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    fee_total   = db.Column(db.Numeric(10,2), nullable=False)

    def __repr__(self):
        return f" Students('{self.first_name}', '{self.second_name}', '{self.email}') "

class Fees(db.Model):
    __tablename__ = 'fees'
    id          = db.Column(db.Integer, primary_key=True)
    fee_total   = db.Column(db.Numeric(10, 2), nullable=False)
   
    def __repr__(self):
        return f"Fee('{self.fee_total}')"
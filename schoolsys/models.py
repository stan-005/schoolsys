from datetime import datetime, timedelta
from schoolsys import db

class Students(db.Model):
    __tablename__ = "students"
    id          = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(100), unique=False, index=True)
    second_name = db.Column(db.String(100), unique=False, index=True)
    fee_paid    = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    fee_total   = db.Column(db.Numeric(10,2), nullable=False)
    grade_id    = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)

    def __repr__(self):
        return f" Students('{self.first_name}', '{self.second_name}', '{self.email}') "

class Fees(db.Model):
    __tablename__ = 'fees'
    id          = db.Column(db.Integer, primary_key=True)
    fee_total   = db.Column(db.Numeric(10, 2), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)
    grade = db.relationship('Grades', backref='fees', lazy=True)
   
    def __repr__(self):
        return f"Fee('{self.fee_total}')"

class Teachers(db.Model):
    __tablename__ = 'teachers'
    id            = db.Column(db.Integer, primary_key=True)
    first_name    = db.Column(db.String(100), unique=False, index=True)
    second_name   = db.Column(db.String(100), unique=False, index=True)
    joined_date   = db.Column(db.DateTime, default=datetime.utcnow)

class Grades(db.Model):
    __tablename__ = 'grade'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100))
    levels        = db.Column(db.String(100))
    students      = db.relationship('Students', backref='grade', lazy=True)

    def count_students(self):
        return len(self.students)

    def get_fee(self):
        grade_fee = Fees.query.filter_by(grade_id=self.id).first()
        if grade_fee:
            return grade_fee.fee_total
        else:
            return 0 
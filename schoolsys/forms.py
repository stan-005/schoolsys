from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, DecimalField,
                    SubmitField, TextAreaField, IntegerField)
from wtforms.validators import (DataRequired, Email, 
                                EqualTo, Length, ValidationError)    
class StudentForm(FlaskForm):
    first_name    = StringField('First Name',  validators=[DataRequired(), Length(min=2, max=20)])
    second_name   = StringField('Second Name', validators=[DataRequired(), Length(min=2, max=20)])
    fee_paid      = DecimalField('Fee Paid', default=0)
    fee_total     = DecimalField('Fee Total', validators=[DataRequired()])
    submit        = SubmitField()

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])

class StudentUpdateForm(FlaskForm):
    first_name    = StringField('First Name',  validators=[DataRequired(), Length(min=2, max=20)])
    second_name   = StringField('Second Name', validators=[DataRequired(), Length(min=2, max=20)])
    fee_paid      = DecimalField('Fee Paid', default=0)
    fee_total     = DecimalField('Fee Total', validators=[DataRequired()])
    submit        = SubmitField()
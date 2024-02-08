from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, DecimalField,
                    SubmitField, TextAreaField, IntegerField, SelectField)
from wtforms.validators import (DataRequired, Email, 
                                EqualTo, Length, ValidationError)    
class StudentForm(FlaskForm):
    first_name    = StringField('First Name',  validators=[DataRequired(), Length(min=2, max=20)])
    second_name   = StringField('Second Name', validators=[DataRequired(), Length(min=2, max=20)])
    grade = SelectField('Grade', coerce=int, validators=[DataRequired()])
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

class TeacherForm(FlaskForm):
    first_name    = StringField('First Name',  validators=[DataRequired(), Length(min=2, max=20)])
    second_name   = StringField('Second Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit        = SubmitField('Hire')

class TeacherUpdateForm(FlaskForm):
    first_name    = StringField('First Name',  validators=[DataRequired(), Length(min=2, max=20)])
    second_name   = StringField('Second Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit        = SubmitField('Update')

class GradesForm(FlaskForm):
    name          = SelectField('Cataegory', validators=[DataRequired()], choices=[('Pre-Primary', 'Pre-Primary'), ('Lower-Primary', 'Lower-Primary'),
                                 ('Upper Primary', 'Upper Primary'),('Lower Secondary', 'Lower Secondary')])
    levels        = SelectField('Grades', choices=[('Pre-Primary 1 (PP1)', 'Pre-Primary 1 (PP1)'), ('Pre-Primary 2 (PP2)', 'Pre-Primary 2 (PP2)'),
                                 ('Grade 1', 'Grade 1'),('Grade 2', 'Grade 2'), ('Grade 3', 'Grade 3'), 
                                 ('Grade 4', 'Grade 4'), ('Grade 5', 'Grade 5'), ('Grade 6', 'Grade 6'),
                                 ('Grade 7', 'Grade 7'), ('Grade 8', 'Grade 8'), ('Grade 9', 'Grade 9')])
    submit        = SubmitField('Add New Class')
    
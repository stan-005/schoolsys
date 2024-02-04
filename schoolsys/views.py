from flask import render_template, url_for, redirect, flash, request
from decimal import Decimal
from schoolsys import app, db
from schoolsys.models import Students, Fees
from schoolsys.forms import (StudentForm, SearchForm, StudentUpdateForm)

#Index
@app.route('/')
def home():
    return render_template('admin_dashboard.html')

@app.route('/admin-student')
def admin_student():
    return render_template('admin_student.html')
# #Add student
@app.route('/students/add', methods=['GET','POST'])
def add_student():
    form    = StudentForm()
    if form.validate():
        try:
            student = Students(
                first_name  = form.first_name.data,
                second_name = form.second_name.data,
                fee_paid    = None if form.fee_paid.data == 0 else form.fee_paid.data,
                fee_total   = None if form.fee_total.data == 0 else form.fee_total.data
            )
            db.session.add(student)
            db.session.commit(),
        except:
            db.session.rollback()
        finally:
            db.session.close()
    return render_template('admin_add_student.html', form=form)

#List of students
@app.route('/students')
def student_list():
    form= SearchForm()
    query = request.args.get('query', default='', type=str)
    if query:
        students = Students.query.filter(
            (Students.first_name.ilike(f'%{query}%')) |
            (Students.second_name.ilike(f'%{query}%'))
        ).all()
    else:
        students = Students.query.all()
    return render_template('admin_view_student.html', students=students, form=form, query=query)

#Student Details

@app.route('/students/<int:student_id>')
def student_detail(student_id):
    student   = db.session.query(Students, Fees).join(Fees, Students.fee_total==Fees.fee_total).filter(Students.id==student_id).all()
    return render_template('student_detail.html', student=student)
   

#Update Students
@app.route('/students/<int:student_id>/update', methods=['GET','POST'])
def update_student(student_id):
    form = StudentUpdateForm()
    student = Students.query.get_or_404(student_id)
    if form.validate():
        fee_paid_decimal = form.fee_paid.data or Decimal(0)
        fee_total_decimal = form.fee_total.data or Decimal(0)
        student.first_name  = form.first_name.data
        student.second_name = form.second_name.data
        student.fee_paid    += fee_paid_decimal
        student.fee_total    = fee_total_decimal
        db.session.commit()
        return redirect(url_for('student_list'))
    return render_template('admin_update_student.html',student=student, form=form)

# #Delete Students
# @app.route('/delete/<int:student_id>', methods=['GET', 'POST'])
# def delete_student(student_id):
#         try:
#             student = Students.query.get_or_404(student_id)
#             db.session.delete(student)
#             db.session.commit()
#         except:
#             db.session.rollback()
#         finally:
#             db.session.close()
#         return redirect(url_for('student_list'))
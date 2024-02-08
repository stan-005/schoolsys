from flask import render_template, url_for, redirect, flash, request
from decimal import Decimal
from schoolsys import app, db
from schoolsys.models import Students, Fees, Teachers, Grades
from schoolsys.forms import (StudentForm, SearchForm, TeacherUpdateForm,
                            StudentUpdateForm, TeacherForm, GradesForm)

#Index
@app.route('/')
def home():
    teachers = Teachers.query.all()
    students = Students.query.all()
    total_teachers = len(teachers)
    total_students = len(students)
    return render_template('admin_dashboard.html', 
                            total_students=total_students, total_teachers=total_teachers)

@app.route('/admin-student')
def admin_student():
    return render_template('admin_student.html')
# #Add student
@app.route('/students/add', methods=['GET','POST'])
def add_student():
    form    = StudentForm()
    form.grade.choices = [(grade.id, grade.levels) for grade in Grades.query.all()]
    if form.validate_on_submit():
        try:
            student = Students(
                first_name  = form.first_name.data,
                second_name = form.second_name.data,
                fee_paid    = None if form.fee_paid.data == 0 else form.fee_paid.data,
                fee_total   = None if form.fee_total.data == 0 else form.fee_total.data,
                grade_id    = form.grade.data
            )
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('student_list'))
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
    if form.validate_on_submit():
        try:
            fee_paid_decimal = form.fee_paid.data or Decimal(0)
            fee_total_decimal = form.fee_total.data or Decimal(0)
            student.first_name  = form.first_name.data
            student.second_name = form.second_name.data
            student.fee_paid    += fee_paid_decimal
            student.fee_total    = fee_total_decimal
            db.session.commit()
            return redirect(url_for('student_list'))
        except:
            db.session.rollback()

    elif request.method == 'GET':
        form.first_name.data = student.first_name
        form.second_name.data = student.second_name
        form.fee_paid.data = student.fee_paid
        form.fee_total.data= student.fee_total
    return render_template('admin_update_student.html',student=student, form=form)

# #Delete Students
@app.route('/delete/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):

    try:
        student = Students.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('student_list'))
    return render_template('admin_view_student.html', student=student)


#### TEACHERS SECTION
@app.route('/admin-teacher')
def admin_teacher():
    return render_template('admin_teacher.html')

# ADD TEACHER
@app.route('/teacher', methods=['GET', 'POST'])
def add_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        try:
            teacher = Teachers(
                first_name = form.first_name.data,
                second_name = form.second_name.data
            )
            db.session.add(teacher)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            db.session.rollback()
        finally:
            db.session.close()
        
    return render_template('admin_add_teacher.html', form=form)

#LIST TEACHERS
@app.route('/teachers_list', methods=['GET', 'POST'])
def teacher_list():
    form= SearchForm()
    query = request.args.get('query', default='', type=str)
    if query:
        teachers = Teachers.query.filter(
            (Teachers.first_name.ilike(f'%{query}%')) |
            (Teachers.second_name.ilike(f'%{query}%'))
        ).all()
    else:
        teachers = Teachers.query.all()
    return render_template('admin_view_teacher.html', teachers=teachers, form=form, query=query)

# Teachers Details
@app.route('/teachers/<int:teachers_id>', methods=['POST', 'GET'])
def individual_teacher(teachers_id):
    teacher = Teachers.query.get_or_404(teachers_id)
    return render_template('teacher_detail.html', teacher=teacher)

#UPDATE TEACHERS
@app.route('/teachers/update/<int:teacher_id>', methods=['POST', 'GET'])
def update_teacher(teacher_id):
    form = TeacherUpdateForm()
    teacher = Teachers.query.get_or_404(teacher_id)
    if form.validate_on_submit():
        try:
            teacher.first_name = form.first_name.data,
            teacher.second_name = form.second_name.data
            db.session.commit()
            return redirect(url_for('teacher_list'))
        except:
            db.session.rollback()
    elif request.method == 'GET':
        form.first_name.data = teacher.first_name
        form.second_name.data = teacher.second_name
    
    return render_template('admin_update_teacher.html', teacher=teacher, form=form)

#Delete Teacher
@app.route('/delete/<int:teacher_id>', methods=['GET', 'POST'])
def delete_teacher(teacher_id):
    try:
        teacher = Students.query.get_or_404(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('student_list'))
    return render_template('admin_view_teacher.html', teacher=teacher)

#GET STUDENTS WITH FEE BALANCE
@app.route('/students/fee_balance', methods=['GET', 'POST'])
def fee_balance_list():
    students = Students.query.all()
    return render_template('students_fee_balance.html', students=students)

# GET THE FEE PAGE
# @app.route('/admin/fee', methods=['GET', 'POST'])
# def vie_fee_page():
#     return render_template('admin_fee.html')

# GRADES
@app.route('/grades', methods=['GET','POST'])
def get_grades():
    grades = Grades.query.all()
    return render_template('grades.html', grades=grades)

# ADD NEW GRAAAAAAADE
@app.route('/new_grade', methods=['GET', 'POST'])
def new_grade():
    form = GradesForm()
    if form.validate_on_submit():
        try:
            grade = Grades(
                name = form.name.data,
                levels = form.levels.data
            )
            db.session.add(grade)
            db.session.commit()
            return redirect(url_for('get_grades'))
        except:
            db.session.rollback()
        finally:
            db.session.close()
    return render_template('admin_add_grade.html', form=form)

# VIEW ALL GRADES IN SCHOOL
@app.route('/grade_list', methods=['GET', 'POST'])
def grade_list():
    grades = Grades.query.all()
    return render_template('admin_view_grades.html', grades=grades)

# SPECIFIC STUDENTS IN EACH GRADE
@app.route('/grades/<grade_name>', methods=['GET', 'POST'])
def students_in_each_grade(grade_name):
    grades = Grades.query.filter_by(name=grade_name).first()
    if grades:
        students = grades.students
    return render_template('students_in_grades.html', grades=grades, students=students)
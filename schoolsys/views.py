from flask import render_template, url_for, redirect, flash, request
from decimal import Decimal
from schoolsys import app, db
from schoolsys.models import Students, Fees, Teachers, Grades
from schoolsys.forms import (StudentForm, SearchForm, TeacherUpdateForm,
                            StudentUpdateForm, TeacherForm, GradesForm,
                            FeeForm)


# STUDENTS SECTION---------------------------------------------------------------------------------------
#Index
@app.route('/')
def home():
    teachers = Teachers.query.all()
    students = Students.query.all()
    total_teachers = len(teachers)
    total_students = len(students)
    
    all_grades = Grades.query.all()
    grades_data = []
    for grade in all_grades:
        total_students_in_grade = grade.students
        total_students_in_grade_count = len(total_students_in_grade)
        total_fee_expected = total_students_in_grade_count * grade.get_fee()
        total_fee_paid = sum(student.fee_paid for student in grade.students)  
        fee_balance = total_fee_expected - total_fee_paid 
        total_students_in_grade = len(total_students_in_grade)
        grades_data.append({'grade': grade, 'total_students': total_students_in_grade,
                            'total_fee_expected': total_fee_expected,
                            'total_fee_paid': total_fee_paid,
                            'fee_balance': fee_balance})
    
    return render_template('admin_dashboard.html', 
                           total_students=total_students, 
                           total_teachers=total_teachers,
                           grades_data=grades_data)

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
    form.grade.choices = [(grade.id, grade.levels) for grade in Grades.query.all()]
    student = Students.query.get_or_404(student_id)
    if form.validate_on_submit():
        try:
            fee_paid_decimal = form.fee_paid.data or Decimal(0)
            fee_total_decimal = form.fee_total.data or Decimal(0)
            student.first_name  = form.first_name.data
            student.second_name = form.second_name.data
            student.fee_paid    += fee_paid_decimal
            student.fee_total    = fee_total_decimal
            student.grade_id     = form.grade.data
            db.session.commit()
            return redirect(url_for('student_list'))
        except:
            db.session.rollback()

    elif request.method == 'GET':
        form.first_name.data = student.first_name
        form.second_name.data = student.second_name
        form.fee_paid.data = student.fee_paid
        form.fee_total.data= student.fee_total
        form.grade.data = student.grade_id
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


#### TEACHERS SECTION------------------------------------------------------------
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


# GRADES SECTION------------------------------------------------------------------------------
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
@app.route('/grades/<grade_ids>', methods=['GET', 'POST'])
def students_in_each_grade(grade_ids):
    form = SearchForm()   
    grades = Grades.query.filter_by(levels=grade_ids).first()
    if grades:
        students = grades.students
        query = request.args.get('query', default='', type=str)
        if query:
            students = Students.query.filter(
            (Students.first_name.ilike(f'%{query}%')) |
            (Students.second_name.ilike(f'%{query}%'))
        ).all()

    else:
        students = []
    return render_template('students_in_grades.html', grades=grades, students=students, form=form, query=query)

# STUDENTS IN SPECIFIC GRADES WITH FEE BALANCE
@app.route('/fee_balance/<grade_id>', methods=['GET'])
def fee_balance_in_grade(grade_id):
    form = SearchForm() 
    grade = Grades.query.get_or_404(grade_id)
    if grade:
        students = Students.query.filter_by(grade_id=grade.id).all()
        students_with_balance = []
        for student in students:
            if student.fee_paid < student.fee_total:
                balance = student.fee_total - student.fee_paid
                students_with_balance.append((student, balance))
        return render_template('admin_view_student_fee_balance_in_grade.html', grade=grade, 
                                students_with_balance=students_with_balance, form=form)
# FEE SECTION ---------------------------------------------------------

@app.route('/fee')
def fee_page():
    return render_template('admin_view_fee.html')

#add fee
@app.route('/add_fee', methods=['GET', 'POST'])
def add_fee():
    form = FeeForm()
    form.grade_level.choices = [(grade.id, grade.levels) for grade in Grades.query.all()]

    if form.validate_on_submit():
        grade_id = form.grade_level.data
        fee_total = form.fee_total.data

        fee_entry = Fees.query.filter_by(grade_id=grade_id).first()
        if fee_entry:
            fee_entry.fee_total = fee_total
        else:
            fee_entry = Fees(grade_id=grade_id, fee_total=fee_total)
            db.session.add(fee_entry)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('admin_add_fee.html', form=form)

#UPDATE FEE
@app.route('/update/<int:fee_id>')
def update_fee(fee_id):
    form = FeeForm()
    fee = Fees.query.get_or_404(fee_id)
    form.grade_level.choices = [(grade.id, grade.levels) for grade in Grades.query.all()]

    if form.validate_on_submit():
        grade_id = form.grade_level.data
        fee_total = form.fee_total.data

        fee_entry = Fees.query.filter_by(grade_id=grade_id).first()
        if fee_entry:
            fee_entry.fee_total = fee_total
        else:
            fee_entry = Fees(grade_id=grade_id, fee_total=fee_total)
            db.session.commit()

        return redirect(url_for('home'))

    return render_template('admin_add_fee.html', form=form)
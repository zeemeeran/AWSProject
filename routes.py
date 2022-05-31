from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
from appinit import app, db
from dbHandler import Student
import uploadS3 

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        student_name = request.form['name']
        student_course = request.form['course']
        student_phone = request.form['phone']
        student_picture = request.form['picture']

        student = Student(student_name, student_course, student_phone, student_picture)

        try:
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error while saving to DB." + str(e))
    else:
        students = Student.query.order_by(Student.student_id).all()
        return render_template('index.html', students=students)
    return render_template('index.html')


@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST':
        student_name = request.form['name']
        student_course = request.form['course']
        student_phone = request.form['phone']
       # student_picture = request.form['picture']

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        filename = secure_filename(file.filename)

        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            status = uploadS3.upload(filename)
            if status == True:
                filepath = 'static/files/' + filename
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f'{filepath} deleted successfully')
                else:
                    print("The file does not exist") 


        student_picture = filename
        student = Student(student_name, student_course, student_phone, student_picture)
        
        try:
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error while saving to DB." + str(e))
    else:      
        return render_template('add.html')


@app.route('/delete/<int:student_id>')
def delete(student_id):
    record_to_delete = Student.query.get_or_404(student_id)

    try:
        db.session.delete(record_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print("Error while delete from DB." + str(e))
        return 'There was a problem deleting the student.'


@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.student_name = request.form['name']
        student.student_course = request.form['course']
        student.student_phone = request.form['phone']
       # student.student_picture = request.form['picture']

        file = request.files['file']
        filename = secure_filename(file.filename)
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            status = uploadS3.upload(filename)
            if status == True:
                filepath = 'static/files/' + filename
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f'{filepath} deleted successfully')
                else:
                    print("The file does not exist") 


        student.student_picture = filename
       
        student = Student(student.student_name, student.student_course, student.student_phone, student.student_picture)

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error while update on DB." + str(e))
            return 'There was a problem updating the student.'

    else:
        return render_template('update.html', student=student)
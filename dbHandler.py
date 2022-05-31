#from flask_sqlalchemy import SQLAlchemy
from appinit import db


class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50))
    student_course = db.Column(db.String(50))
    student_phone = db.Column(db.String(20))
    student_picture = db.Column(db.String(200))

    def __init__(self, student_name, student_course, student_phone, student_picture):
        self.student_name = student_name
        self.student_course = student_course
        self.student_phone = student_phone
        self.student_picture = student_picture

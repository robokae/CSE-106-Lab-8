# Database code
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin

# UserMixin = methods that are needed for flask login

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# class User(UserMixin, db.Model):
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
	teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))


class Teacher(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	
	user = db.relationship('User', backref='teacher', uselist=False)


class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String, nullable=False)

	user = db.relationship('User', backref='student', uselist=False)
	courses = db.relationship('Enrollment', back_populates='student')


class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	course_name = db.Column(db.String, unique=True, nullable=False)
	teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
	number_enrolled = db.Column(db.Integer, nullable=False)
	capacity = db.Column(db.Integer, nullable=False)
	time = db.Column(db.String, nullable=False)

	teacher = db.relationship('Teacher', backref=db.backref('teachers', lazy=True))
	students = db.relationship('Enrollment', back_populates='course')


class Enrollment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
	grade = db.Column(db.Integer, nullable=False)

	student = db.relationship('Student', back_populates='courses')
	course = db.relationship('Course', back_populates='students')

	
	
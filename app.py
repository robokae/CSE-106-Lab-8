# Main application code
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

# SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Flask Admin
app.config['FLASK_ADMIN_SWATCH'] = 'Cyborg'
app.config['SECRET_KEY'] = 'testkey'

db = SQLAlchemy(app)
admin = Admin(app)
login = LoginManager(app)
cors = CORS(app)

from db import User, Teacher, Student, Course, Enrollment

# -------- Admin ----------
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Enrollment, db.session))

# -------- Login ----------
# LoginManager = instance of login
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/", methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        auxUsername = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=auxUsername).first()

        if user is None or not user.check_password(password):
                return render_template("login.html")

        login_user(user)

        if user.student_id is None:
            teacher = Teacher.query.filter_by(id=user.teacher_id).first()
            return redirect(url_for('instructor', name = teacher.name))
        else:
            student = Student.query.filter_by(id=user.student_id).first()
            return redirect(url_for('student', name=student.name))

    else:
        if current_user.is_authenticated:
            if current_user.student_id is None:
                teacher = Teacher.query.filter_by(id=current_user.teacher_id).first()
                return redirect(url_for('instructor', name = teacher.name))
            else:
                student = Student.query.filter_by(id=current_user.student_id).first()
                return redirect(url_for('student', name=student.name))

        return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/student/<name>", methods = ['POST', 'GET'])
# @login_required
def student(name):
    student_name = name

    try_data = []
        
    # get all courses the student is enrolled in
    if request.method == 'GET':
        stuQ = Student.query.filter_by(name=student_name).first()
        stuQC = stuQ.courses

        for i in range(len(stuQC)):
            temp = {
                'name':stuQC[i].course.course_name,
                'instructor':stuQC[i].course.teacher.name,
                'time':stuQC[i].course.time,
                'enrollment':(str(stuQC[i].course.number_enrolled) + "/" + str(stuQC[i].course.capacity))
            }
            try_data.append(temp)
        
    # add or remove a course
    elif request.method == 'POST': 
        course_name = request.form.get('course_name')
        enroll_option = request.form.get('enroll_option')

        stuQ = Student.query.filter_by(name=student_name).first()
        courseReqNm = course_name
        courseReq = Course.query.filter_by(course_name = courseReqNm).first()

        if enroll_option == 'add':
            # update the enrollment count
            Course.query.filter_by(course_name = courseReqNm).update({'number_enrolled': (Course.number_enrolled + 1)})
            newCourseStu = Enrollment(student_id = stuQ.id, course_id = courseReq.id, grade = "")
            db.session.add(newCourseStu)

        elif enroll_option == 'remove':
            Course.query.filter_by(course_name = courseReqNm).update({'number_enrolled': (Course.number_enrolled - 1)})
            enrollmentReq = Enrollment.query.filter_by(student_id = stuQ.id, course_id = courseReq.id).first()
            
            db.session.delete(enrollmentReq)


        db.session.commit()
    
    return render_template("student.html", student_name = student_name, data = try_data)


@app.route("/instructor/<name>")
# @login_required
def instructor(name):
    instructor_name = name
    
    tea_data = []
    teaQ = Teacher.query.filter_by(name=instructor_name).first()
    teaQC = Course.query.filter_by(teacher_id = teaQ.id).all()
    for i in range(len(teaQC)):
        temp = {
            'name':teaQC[i].course_name,
            'instructor':instructor_name,
            'time':teaQC[i].time,
            'enrollment':(str(teaQC[i].number_enrolled) + "/" + str(teaQC[i].capacity))
        }
        tea_data.append(temp)
    
    return render_template("instructor.html", instructor_name = instructor_name, data = tea_data)

@app.route("/instructor/<name>/<course>", methods = ['GET', 'POST'])
def specific_course(name, course, student = None):
    instructor_name = name
    instructor_course = course

    tea_course_data = []
    teaQ = Teacher.query.filter_by(name=instructor_name).first()
    teaQC = Course.query.filter_by(teacher_id = teaQ.id, course_name = instructor_course).first()

    print(teaQC)

    if request.method == 'GET':
        # Displays grades for a specific course
        for j in range(len(teaQC.students)):
            temp1 = {
                'name':teaQC.students[j].student.name,
                'grade':teaQC.students[j].grade
            }
            tea_course_data.append(temp1)

    if request.method == 'POST':
        student_id = Student.query.filter_by(name = request.args.get('student')).first().id
        course_id = Course.query.filter_by(course_name = instructor_course).first().id

        Enrollment.query.filter_by(student_id = student_id, course_id = course_id).update({'grade': (request.form.get('new_grade'))})
        db.session.commit()

        for j in range(len(teaQC.students)):
            temp1 = {
                'name':teaQC.students[j].student.name,
                'grade':teaQC.students[j].grade
            }
            tea_course_data.append(temp1)
    

    return render_template("specificCourse.html", instructor_name = instructor_name, instructor_course = instructor_course, data = tea_course_data)
    

@app.route("/enrolled/<name>")
def enrolled(name, methods = ['POST', 'GET']):
    student_name = name
    try_data = []
    if request.method == 'GET':
        stuQ = Student.query.filter_by(name=student_name).first()
        stuQC = stuQ.courses

        for i in range(len(stuQC)):
            temp = {
                'name':stuQC[i].course.course_name,
                'instructor':stuQC[i].course.teacher.name,
                'time':stuQC[i].course.time,
                'enrollment':(str(stuQC[i].course.number_enrolled) + "/" + str(stuQC[i].course.capacity))
            }
            try_data.append(temp)
    
    return jsonify(try_data)

@app.route("/courses")
def courses():
    try_data = []
    courseQ = Course.query.all()
    for i in range(len(courseQ)):
        temp = {
            'name':courseQ[i].course_name,
            'instructor':courseQ[i].teacher.name,
            'time':courseQ[i].time,
            'enrollment':(str(courseQ[i].number_enrolled) + "/" + str(courseQ[i].capacity))
        }
        try_data.append(temp)
    return jsonify(try_data)

if __name__ == "__main__":
    app.run(debug=True)
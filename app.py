# Main application code
from flask import Flask, render_template, request, url_for, redirect

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from db import User, Teacher, Student, Course, Enrollment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# -------- Admin ----------
admin = Admin(app)

app.config['FLASK_ADMIN_SWATCH'] = 'Cyborg'

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Enrollment, db.session))

# -------- Login ----------
# LoginManager = instance of login

login = LoginManager(app)
login.login_view = 'login'

app.config['SECRET_KEY'] = 'testkey'

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)



# @app.route("/")
# def base():
#     return render_template("base.html")


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


@app.route("/student/<name>")
@login_required
def student(name):
    student_name = name
    try_data = []
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


    # CODE TO DISPLAY ALL COURSES 
    # courseQ = Course.query.all()
    # for i in range(len(courseQ)):
    #     temp = {
    #         'name':courseQ[i].course_name,
    #         'instructor':courseQ[i].teacher.name,
    #         'time':courseQ[i].time,
    #         'enrollment':(str(courseQ[i].number_enrolled) + "/" + str(courseQ[i].capacity))
    #     }
    #     try_data.append(temp)
    # # CODE TO DISPLAY ALL COURSES (END)
    
    return render_template("student.html", student_name = student_name, data = try_data)

    # ENROLL APP ROUTE HERE (Includes the DISPLAY ALL COURSES functionality for add and drop purposes)-------------------------------------------------------------------------------------
    # @app.route("/student/<name>/enroll", methods = ["POST", "GET"])
    # def enroll(name):
    #     student_name = name
    #     try_data = []
    #     if request.method == "GET":
    #         courseQ = Course.query.all()
    #         for i in range(len(courseQ)):
    #             temp = {
    #                 'name':courseQ[i].course_name,
    #                 'instructor':courseQ[i].teacher.name,
    #                 'time':courseQ[i].time,
    #                 'enrollment':(str(courseQ[i].number_enrolled) + "/" + str(courseQ[i].capacity))
    #             }
    #             try_data.append(temp)
    #     elif request.method == "POST":
    #         stuQ = Student.query.filter_by(name=student_name).first()
    #         courseReqNm = ""
    #         courseReq = Course.query.filter_by(course_name = courseReqNm).first()
    #         newCourseStu = Enrollment(student_id = stuQ.id, course_id = courseReq.id, grade = "")
    #         db.session.add(newCourseStu)
    #         db.session.commit()
    #     return jsonify(try_data)
    # ENROLL APP ROUTE HERE (END)----------------------------------------------------------------------------------------------------------------------------------------------------------


@app.route("/instructor/<name>")
@login_required
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
    # CODE TO DISPLAY TABLE OF STUDENTS AND THEIR GRADES BASED OFF OF THE SELECTED CLASS
    # tea_courses_data = {}
    # for i in range(len(teaQC)):
    #   courseT = []
    #   for j in range(len(teaQC[i].students)):
    #       temp1 = {
    #           'student name':teaQC[i].students[j].student.name,
    #           'grade':teaQC[i].students[j].grade
    #       }
    #       courseT.append(temp1)
    #   tea_courses_data[teaQC[i].course_name] = courseT
    # returnData = tea_course_data[courseName] <- this line of code would work off of the course clicked by the teacher, returning the table of students and grades pertaining to the course labeled courseName
    # CODE TO DISPLAY TABLE OF STUDENTS AND THEIR GRADES BASED OFF OF THE SELECTED CLASS (END)
    return render_template("instructor.html", instructor_name = instructor_name, data = tea_data)

    # EDIT GRADES PAGE FOR INSTRUCTOR HERE----------------------------------------------------------------------------------------------------------------------
    # @app.route("/instructor/<name>/<course>")
    # def instructorCourses(name, course):
    #     instructor_name = name
    #     teaQ = Teacher.query.filter_by(name=instructor_name).first()
    #     teaQC = Course.query.filter_by(teacher_id = teaQ.id).all()
    #     tea_courses_data = {}
    #     for i in range(len(teaQC)):
    #       courseT = []
    #       for j in range(len(teaQC[i].students)):
    #           temp1 = {
    #               'student name':teaQC[i].students[j].student.name,
    #               'grade':teaQC[i].students[j].grade
    #           }
    #           courseT.append(temp1)
    #       tea_courses_data[teaQC[i].course_name] = courseT
    #       returnData = tea_courses_data[course]
    #       return render_template("instructor.html", instructor_name = instructor_name, data = tea_data)
    # EDIT GRADES PAGE FOR INSTRUCTOR HERE (END) -------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
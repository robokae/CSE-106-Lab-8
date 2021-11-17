# Main application code
from flask import Flask, render_template, request, url_for, redirect
from db import db, User, Teacher, Student, Course, Enrollment, app

# app = Flask(__name__)

# @app.route("/")
# def base():
#     return render_template("base.html")

@app.route("/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        userQ = User.query.filter_by(username = user).first()
        if type(userQ) is type(None):
            return render_template("login.html")
        if userQ.student_id == None:
            nameQ = Teacher.query.filter_by(id = userQ.teacher_id).first()
            return redirect(url_for("instructor", name = nameQ.name))
        elif userQ.teacher_id == None:
            nameQ = Student.query.filter_by(id = userQ.student_id).first()
            return redirect(url_for("student", name = nameQ.name))
    else:
        return render_template("login.html")

@app.route("/student/<name>")
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

# USELESS CODE THUS FAR
# @app.route("/index")
# def index():
#     return render_template("grade/index.html")

# @app.route("/update")
# def update():
#     return render_template("grade/update.html")
# USELESS CODE THUS FAR (END)

if __name__ == "__main__":
    app.run()
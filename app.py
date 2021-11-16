# Main application code
from flask import Flask, render_template, request, url_for, redirect
from db import db, User, Teacher, Student, Course, Enrollment

app = Flask(__name__)

# @app.route("/")
# def base():
#     return render_template("base.html")

@app.route("/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("student", name = user))
    else:
        return render_template("login.html")

@app.route("/student/<name>")
def student(name):
    sample_data = [
        {
            'name': 'BIO 1',
            'instructor': 'John Smith',
            'time': 'MWF 11:00am - 12:15pm',
            'enrollment': '65/200'
        },
        {
            'name': 'PHYS 10',
            'instructor': 'Jane Doe',
            'time': 'TR 5:00pm - 6:15pm',
            'enrollment': '92/150'
        }
    ]
    student_name = name
    # GOOD CODE AS FAR AS I KNOW, PROBLEM IS SQLALCHEMY AT THE MOMENT
    # try_data = []
    # stuQ = Student.query.filter_by(name=student_name).first()
    # stuQC = stuQ.courses
    # for i in range(len(stuQC)):
    #     temp = {
    #         'name':stuQC[i].course.course_name,
    #         'instructor':stuQC[i].course.teacher.name,
    #         'time':stuQC[i].course.time,
    #         'enrollment':(str(stuQC[i].course.number_enrolled) + "/" + str(stuQC[i].course.capacity))
    #     }
    #     try_data.append(temp)
    # print(try_data)
    
    # TESTING ERROR BLOCK OF CODE BELOW
    # testdb = Student.query.all()
    # print("------------------- STUDENTS -------------------")
    # for student in testdb:
	#     print(student.id, student.name, student.user, student.courses)
    
    return render_template("student.html", student_name = student_name, data = sample_data)
    # return render_template("student.html", student_name = student_name, data = try_data)

@app.route("/instructor/<name>")
def instructor(name):
    instructor_name = name
    return render_template("instructor.html", instructor_name = instructor_name)

@app.route("/index")
def index():
    return render_template("grade/index.html")

@app.route("/update")
def update():
    return render_template("grade/update.html")

if __name__ == "__main__":
    app.run()
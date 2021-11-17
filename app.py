# Main application code
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

sample_enrolled_data = [
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

sample_courses_data = [
    {
        'option': 'Remove',
        'name': 'BIO 1',
        'instructor': 'John Smith',
        'time': 'MWF 11:00am - 12:15pm',
        'enrollment': '65/200'
    },
    {
        'option': 'Add',
        'name': 'BIO 10',
        'instructor': 'John Smith',
        'time': 'TR 12:00pm - 1:15pm',
        'enrollment': '82/150'
    },
    {
        'option': 'Add',
        'name': 'BIO 122',
        'instructor': 'John Smith',
        'time': 'MW 2:00pm - 3:15pm',
        'enrollment': '102/120'
    },
    {
        'option': 'Remove',
        'name': 'PHYS 10',
        'instructor': 'Jane Doe',
        'time': 'TR 5:00pm - 6:15pm',
        'enrollment': '92/150'
    }
]

sample_instructor_data = [
    {
        'name': 'BIO 1',
        'instructor': 'John Smith',
        'time': 'MWF 11:00am - 11:50am',
        'enrollment': '65/200'
    },
    {
        'name': 'BIO 10',
        'instructor': 'John Smith',
        'time': 'TR 12:00pm - 1:15pm',
        'enrollment': '82/150'
    },
    {
        'name': 'BIO 122',
        'instructor': 'John Smith',
        'time': 'MW 2:00pm - 3:15pm',
        'enrollment': '102/120'
    }
]

sample_instructor_course_data = [
    {
        'name': 'John Smith',
        'grade': 93
    },
    {
        'name': 'Alice Jones',
        'grade': 94
    },
    {
        'name': 'Mary Chen',
        'grade': 95
    },
    {
        'name': 'David',
        'grade': 96
    },
    {
        'name': 'Santosh',
        'grade': 97
    }
]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/student/<name>")
def student(name):
    student_name = name
    return render_template("student.html", student_name = student_name)

@app.route("/instructor/<name>")
def instructor(name):
    instructor_name = name
    return render_template("instructor.html", instructor_name = instructor_name, data = sample_instructor_data)

@app.route("/instructor/<name>/<course>", methods = ['GET', 'POST'])
def specific_course(name, course, student = None):
    instructor_name = name
    instructor_course = course

    if request.method == 'POST':
        student_name = request.args.get('student')
        print('student name is %s' % student_name)
        for s in sample_instructor_course_data:
            if s['name'] == student_name:
                s['grade'] = request.form.get('new_grade')

    return render_template("specificCourse.html", instructor_name = instructor_name, instructor_course = instructor_course, data = sample_instructor_course_data)

@app.route("/enrolled/<name>")
def enrolled(name):
    # return array of json
    return jsonify(sample_enrolled_data)

@app.route("/courses")
def courses():
    return jsonify(sample_courses_data)

@app.route("/index")
def index():
    return render_template("grade/index.html")

@app.route("/update")
def update():
    return render_template("grade/update.html")

if __name__ == "__main__":
    app.run()
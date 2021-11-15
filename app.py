# Main application code
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

# @app.route("/")
# def base():
#     return render_template("base.html")

@app.route("/")
def login():
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
    return render_template("student.html", student_name = student_name, data = sample_data)

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
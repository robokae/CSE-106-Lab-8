# Main application code
from flask import Flask, render_template, request, url_for, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user
from db import User, Teacher, Student, Course, Enrollment, db

# from flask_admin import Admin, AdminIndexView
# from flask_login import LoginManager, current_user, login_user, logout_user
# from flask_login.utils import login_required
# from flask_sqlalchemy.model import Model
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
    return User.get_id(user_id)
# -------------------------

# @app.route("/")
# def base():
#     return render_template("base.html")

# -------- Admin ----------
# class UserView(ModelView):
#     def is_accessible(self):
#         return True

# class TeacherView(ModelView):
#     def is_accessible(self):
#         return True

# class StudentView(ModelView):
#     def is_accessible(self):
#         return True

# class CourseView(ModelView):
#     def is_accessible(self):
#         return True

# class EnrollmentView(ModelView):
#     def is_accessible(self):
#         return True

# --------------------------


@app.route("/", methods = ["POST", "GET"])
def login():

        if request.method == 'POST':
        # if current_user.is_authenticated:
        #     if current_user.student_id is None:
        #         return redirect(url_for('instructor'))
        #     else:
        #         return redirect(url_for('student'))

            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()

            if not user is None or not user.check_password(password):
                    return redirect(url_for('login'))

            login_user(user)

            if user.student_id is None:
                redirect(url_for('instructor'))
            else:
                redirect(url_for('student'))


# @app.route('/logout')
# def logout():
#     logout_user


@app.route("/student/<name>")
# @login_required
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
# @login_required
def instructor(name):
    instructor_name = name
    return render_template("instructor.html", instructor_name = instructor_name)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/update")
def update():
    return render_template("update.html")

if __name__ == "__main__":
    app.run(debug=True)
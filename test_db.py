from db import db, User, Teacher, Student, Course, Enrollment

users = User.query.all()
teachers = Teacher.query.all()
students = Student.query.all()
courses = Course.query.all()
enrollments = Enrollment.query.all()

print("------------------- USERS -------------------")
for user in users:
	print(user.id, user.username, user.password, user.student_id, user.teacher_id)

print("------------------- TEACHERS -------------------")
for teacher in teachers:
	print(teacher.id, teacher.name, teacher.user)

print("------------------- STUDENTS -------------------")
for student in students:
	print(student.id, student.name, student.user, student.courses)

print("------------------- COURSES -------------------")
for course in courses:
	print(course.id, course.course_name, course.teacher_id, course.teacher.name, course.number_enrolled, course.capacity, course.time, course.students)

print("------------------- ENROLLMENT -------------------")
for enrollment in enrollments:
	print(enrollment.id, enrollment.grade, enrollment.student.name, enrollment.course.course_name)

print("---------------------Play Testing------------------")
namStu = "John Stuart"
stuJose = Student.query.filter_by(name=namStu).first()
# print(stuJose.name, stuJose.courses)
print(stuJose.name)
print("")
stuC = stuJose.courses
# print(stuC[0].course.course_name)
for i in range(len(stuC)):
	print(stuC[i].course.course_name)
	print(stuC[i].course.time)
	print(stuC[i].course.teacher.name)
	print(str(stuC[i].course.number_enrolled) + "/" + str(stuC[i].course.capacity))
	print("")

namTea = "Ammon Hepworth"
teaAm = Teacher.query.filter_by(name=namTea).first()
print(teaAm.name)
print("")
teaAMC = Course.query.filter_by(teacher_id = teaAm.id).all()
for i in range(len(teaAMC)):
	print(teaAMC[i].course_name)
	print(teaAMC[i].time)
	print(str(teaAMC[i].number_enrolled) + "/" + str(teaAMC[i].capacity))
print("")
# print(teaAMC[0].students[0].student.name)
for i in range(len(teaAMC)):
	print(teaAMC[i].course_name)
	for j in range(len(teaAMC[i].students)):
		print(teaAMC[i].students[j].student.name)
		print(teaAMC[i].students[j].grade)
	print("")

userName = "ahepwor"
userNameQ = User.query.filter_by(username = userName).first()
if type(userNameQ) is type(None):
	print("No")
else:
	print(userNameQ.teacher_id)
	teachAm = Teacher.query.filter_by(id = userNameQ.teacher_id).first()
	print(teachAm.name)
# userNameQ = User.query.filter_by(username = userName).first()
# print(userNameQ.teacher_id)
# teachAm = Teacher.query.filter_by(id = userNameQ.teacher_id).first()
# print(teachAm.name)
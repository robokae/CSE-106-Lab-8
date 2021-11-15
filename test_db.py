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
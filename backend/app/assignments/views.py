from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from core.models import Profile
from assignments.models import Assignment, Tasklist
import json


# return all assignments for a given teacher
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_quizzes_for_teacher(request):
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")

    response = {"teacher": request.query_params.get('teacher'), "assignments": []}
    # get all assignments + translate to expected response type
    assignments = Assignment.objects.filter(teacher=Profile.objects.get(username=request.query_params.get('teacher')))
    for assignment in assignments:
        assignmentJson = {"students": [], "quizName": assignment.quizName, "quizData": json.loads(assignment.quizData)}
        for student in assignment.students.all():
            assignmentJson["students"].append(student.username)
        response["assignments"].append(assignmentJson)

    return Response(response)


# return all assignments for a given student.
# Expects query param "student" with student username
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_quizzes_for_student(request):
    if request.query_params.get('student') is None:
        raise Exception("Query param 'student' must be passed")

    student_username = request.query_params.get('student')
    response = {"student": student_username, "assignments": []}
    # get all assignments + translate to expected response type
    assignments = Assignment.objects.filter(students__username=student_username)
    for assignment in assignments:
        assignmentJson = {"teacher": assignment.teacher.username, "quizName": assignment.quizName, "quizData": json.loads(assignment.quizData)}
        response["assignments"].append(assignmentJson)

    return Response(response)


# Save assignments
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def save_quiz(request):
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")
    if request.query_params.get('students') is None:
        raise Exception("Query param 'students' must be passed")

    # parse data
    teacher_username = request.query_params.get('teacher')
    student_usernames = request.query_params.get('students').split(",")
    request_as_json = json.loads(request.body)
    quiz_name = request_as_json['quizName']
    quiz_data = json.dumps(request_as_json['quizData'])

    # create database entry + add all data
    teacher_user = Profile.objects.get(username=teacher_username)
    assignment = Assignment(teacher=teacher_user, quizName=quiz_name, quizData=quiz_data)
    assignment.save()
    for student_username in student_usernames:
        student = Profile.objects.get(username=student_username)
        assignment.students.add(student)
        assignment.save()

    return Response({"status": "SUCCESS"})


# Delete assignments
@api_view(['DELETE'])
@permission_classes([])
@authentication_classes([])
def remove_quiz_for_teacher(request):
    if request.query_params.get('quizName') is None:
        raise Exception("Query param 'quizName' must be passed")
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")

    Assignment.objects.filter(quizName=request.query_params.get('quizName')).delete()

    response = {"teacher": request.query_params.get('teacher'), "assignments": []}
    # get all assignments + translate to expected response type
    assignments = Assignment.objects.filter(teacher=Profile.objects.get(username=request.query_params.get('teacher')))
    for assignment in assignments:
        assignmentJson = {"students": [], "quizName": assignment.quizName, "quizData": json.loads(assignment.quizData)}
        for student in assignment.students.all():
            assignmentJson["students"].append(student.username)
        response["assignments"].append(assignmentJson)

    return Response(response)


# Delete assignments
@api_view(['DELETE'])
@permission_classes([])
@authentication_classes([])
def remove_quiz_for_student(request):
    if request.query_params.get('quizName') is None:
        raise Exception("Query param 'quizName' must be passed")
    if request.query_params.get('student') is None:
        raise Exception("Query param 'student' must be passed")

    Assignment.objects.filter(quizName=request.query_params.get('quizName')).delete()

    student_username = request.query_params.get('student')
    response = {"student": student_username, "assignments": []}
    # get all assignments + translate to expected response type
    assignments = Assignment.objects.filter(students__username=student_username)
    for assignment in assignments:
        assignmentJson = {"teacher": assignment.teacher.username, "quizName": assignment.quizName, "quizData": json.loads(assignment.quizData)}
        response["assignments"].append(assignmentJson)

    return Response(response)


# return single quiz for a given quiz name and teacher
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_single_quiz_for_teacher(request):
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")
    if request.query_params.get('quizName') is None:
        raise Exception("Query param 'quizName' must be passed")

    quiz = Assignment.objects.filter(teacher=Profile.objects.get(username=request.query_params.get('teacher'))).get(
        quizName=request.query_params.get('quizName'))
    students = [{"id": student.username, "name": student.first_name + " " + student.last_name} for student
                in quiz.students.all()]
    response = {"teacher": request.query_params.get('teacher'), "students": students, "quizName": quiz.quizName,
                "quizData": json.loads(quiz.quizData)}

    return Response(response)


# return single quiz for a given quiz name and student
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_single_quiz_for_student(request):
    if request.query_params.get('student') is None:
        raise Exception("Query param 'student' must be passed")
    if request.query_params.get('quizName') is None:
        raise Exception("Query param 'quizName' must be passed")

    quiz = Assignment.objects.filter(students__username=Profile.objects.get(username=request.query_params.get('student')))\
        .get(quizName=request.query_params.get('quizName'))
    response = {"student": request.query_params.get('student'), "teacher": quiz.teacher, "quizName": quiz.quizName,
                "quizData": json.loads(quiz.quizData)}

    return Response(response)


# return all tasklists for a given teacher
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_tasklists_for_teacher(request):
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")

    response = {"teacher": request.query_params.get('teacher'), "tasklists": []}
    # get all tasklists + translate to expected response type
    tasklists = Tasklist.objects.filter(teacher=Profile.objects.get(username=request.query_params.get('teacher')))
    for tasklist in tasklists:
        tasklistJson = {"students": [], "tasklistName": tasklist.tasklistName, "tasklistData": json.loads(tasklist.tasklistData)}
        for student in tasklist.students.all():
            tasklistJson["students"].append(student.username)
        response["tasklists"].append(tasklistJson)

    return Response(response)


# return all tasklists for a given student.
# Expects query param "student" with student username
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_tasklists_for_student(request):
    if request.query_params.get('student') is None:
        raise Exception("Query param 'student' must be passed")

    student_username = request.query_params.get('student')
    response = {"student": student_username, "tasklists": []}
    # get all tasklists + translate to expected response type
    tasklists = Tasklist.objects.filter(students__username=student_username)
    for tasklist in tasklists:
        tasklistJson = {"teacher": tasklist.teacher.username, "tasklistName": tasklist.tasklistName, "tasklistData": json.loads(tasklist.tasklistData)}
        response["tasklists"].append(tasklistJson)

    return Response(response)


# Save tasklist
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def save_tasklist(request):
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")
    if request.query_params.get('students') is None:
        raise Exception("Query param 'students' must be passed")

    # parse data
    teacher_username = request.query_params.get('teacher')
    student_usernames = request.query_params.get('students').split(",")
    request_as_json = json.loads(request.body)
    tasklist_name = request_as_json['tasklistName']
    tasklist_data = json.dumps(request_as_json['tasklistData'])

    # create database entry + add all data
    teacher_user = Profile.objects.get(username=teacher_username)
    tasklist = Tasklist(teacher=teacher_user, tasklistName=tasklist_name, tasklistData=tasklist_data)
    tasklist.save()
    for student_username in student_usernames:
        student = Profile.objects.get(username=student_username)
        tasklist.students.add(student)
        tasklist.save()

    return Response({"status": "SUCCESS"})


# Delete tasklists
@api_view(['DELETE'])
@permission_classes([])
@authentication_classes([])
def remove_tasklist_for_teacher(request):
    if request.query_params.get('tasklistName') is None:
        raise Exception("Query param 'tasklistName' must be passed")
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")

    Tasklist.objects.filter(tasklistName=request.query_params.get('tasklistName')).delete()

    response = {"teacher": request.query_params.get('teacher'), "tasklists": []}
    # get all tasklists + translate to expected response type
    tasklists = Tasklist.objects.filter(teacher=Profile.objects.get(username=request.query_params.get('teacher')))
    for tasklist in tasklists:
        tasklistJson = {"students": [], "tasklistName": tasklist.tasklistName, "tasklistData": json.loads(tasklist.tasklistData)}
        for student in tasklist.students.all():
            tasklistJson["students"].append(student.username)
        response["tasklists"].append(tasklistJson)

    return Response(response)


# Delete tasklist
@api_view(['DELETE'])
@permission_classes([])
@authentication_classes([])
def remove_tasklist_for_student(request):
    if request.query_params.get('tasklistName') is None:
        raise Exception("Query param 'tasklistName' must be passed")
    if request.query_params.get('student') is None:
        raise Exception("Query param 'student' must be passed")

    Tasklist.objects.filter(tasklistName=request.query_params.get('tasklistName')).delete()

    student_username = request.query_params.get('student')
    response = {"student": student_username, "tasklists": []}
    # get all tasklists + translate to expected response type
    tasklists = Tasklist.objects.filter(students__username=student_username)
    for tasklist in tasklists:
        tasklistJson = {"teacher": tasklist.teacher.username, "tasklistName": tasklist.tasklistName, "tasklistData": json.loads(tasklist.tasklistData)}
        response["tasklists"].append(tasklistJson)

    return Response(response)


# return single tasklist for a given tasklist name and teacher
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_single_tasklist_for_teacher(request):
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")
    if request.query_params.get('tasklistName') is None:
        raise Exception("Query param 'tasklistName' must be passed")

    tasklist = Tasklist.objects.filter(teacher=Profile.objects.get(username=request.query_params.get('teacher'))).get(
        tasklistName=request.query_params.get('tasklistName'))
    students = [{"id": student.username, "name": student.first_name + " " + student.last_name} for student
                in tasklist.students.all()]
    response = {"teacher": request.query_params.get('teacher'), "students": students, "tasklistName":
        tasklist.tasklistName, "tasklistData": json.loads(tasklist.tasklistData)}

    return Response(response)


# return single quiz for a given tasklist name and student
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_single_tasklist_for_student(request):
    if request.query_params.get('student') is None:
        raise Exception("Query param 'student' must be passed")
    if request.query_params.get('tasklistName') is None:
        raise Exception("Query param 'tasklistName' must be passed")

    tasklist = Tasklist.objects.filter(students_username=Profile.objects.get(username=request.query_params.get('student')))\
        .get(tasklistName=request.query_params.get('tasklistName'))
    response = {"student": request.query_params.get('student'), "teacher": tasklist.teacher, "tasklistName":
        tasklist.tasklistName, "tasklistData": json.loads(tasklist.tasklistData)}

    return Response(response)


# Update existing tasklist for teacher
@api_view(['PUT'])
@permission_classes([])
@authentication_classes([])
def update_tasklist_for_teacher(request):
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")
    if request.query_params.get('tasklistName') is None:
        raise Exception("Query param 'tasklistName' must be passed")

    # parse data
    teacher_username = request.query_params.get('teacher')
    teacher_user = Profile.objects.get(username=teacher_username)

    request_as_json = json.loads(request.body)
    tasklist_data = json.dumps(request_as_json)

    Tasklist.objects.filter(teacher=teacher_user, tasklistName=request.query_params.get('tasklistName'))\
        .update(tasklistData=tasklist_data)

    return Response({"status": "SUCCESS"})


# Update existing tasklist for student
@api_view(['PUT'])
@permission_classes([])
@authentication_classes([])
def update_tasklist_for_student(request):
    if request.query_params.get('student') is None:
        raise Exception("Query param 'student' must be passed")
    if request.query_params.get('tasklistName') is None:
        raise Exception("Query param 'tasklistName' must be passed")

    student_username = request.query_params.get('student')
    student_user = Profile.objects.get(username=student_username)

    request_as_json = json.loads(request.body)
    tasklist_data = json.dumps(request_as_json)

    Tasklist.objects.filter(students_username=student_user, tasklistName=request.query_params.get('tasklistName'))\
        .update(tasklistData=tasklist_data)

    return Response({"status": "SUCCESS"})


# Returns a list of a teacher's students
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_students(request):
    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")

    teacher = Profile.objects.get(username=request.query_params.get('teacher'))

    if teacher.account_type == 'STUDENT':
        raise Exception("User with username " + teacher.username + " is a student account. They do not have students")

    response = {"students": []}
    for student in teacher.students.all():
        student_name = student.first_name + ' ' + student.last_name
        response["students"].append((student.username, student_name))

    return Response(response)


# Returns a list of a student's teachers
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_teachers(request):
    if request.query_params.get('student') is None:
        raise Exception("Query param 'student' must be passed")

    student = Profile.objects.get(username=request.query_params.get('student'))

    if student.account_type == 'TEACHER':
        raise Exception("User with username " + student.username + " is a teacher account. They do not have teachers")

    response = {"teachers": []}
    for teacher in student.teachers.all():
        teacher_name = teacher.first_name + ' ' + teacher.last_name
        response["teachers"].append((teacher.username, teacher_name))

    return Response(response)


# Add a student to a teacher's students
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def add_students(request):

    if request.query_params.get('teacher') is None:
        raise Exception("Query param 'teacher' must be passed")
    if request.query_params.get('students') is None:
        raise Exception("Query param 'students' must be passed")

    teacher = Profile.objects.get(username=request.query_params.get('teacher'))

    if teacher.account_type == "STUDENT":
        raise Exception("User with username " + teacher.username + " is not a teacher account")

    for student_username in request.query_params.get('students').split(","):
        student = Profile.objects.get(username=student_username)
        if student.account_type == "TEACHER":
            raise Exception("User with username " + student.username + " is not a student account")
        teacher.students.add(student)
        student.teachers.add(teacher)

    return Response({"status": "SUCCESS"})

from django.urls import path
from .views import get_quizzes_for_student, get_quizzes_for_teacher, \
    save_quiz, remove_quiz_for_teacher, remove_quiz_for_student, get_single_quiz_for_teacher,\
    get_single_quiz_for_student, get_tasklists_for_teacher, get_tasklists_for_student, \
    save_tasklist, remove_tasklist_for_teacher, remove_tasklist_for_student, \
    get_single_tasklist_for_teacher, get_single_tasklist_for_student, update_tasklist_for_teacher,\
    update_tasklist_for_student, get_students, get_teachers, add_students


urlpatterns = [
    path('teacher/quizzes', get_quizzes_for_teacher),
    path('student/quizzes', get_quizzes_for_student),
    path('save/quiz', save_quiz),
    path('teacher/remove/quiz', remove_quiz_for_teacher),
    path('student/remove/quiz', remove_quiz_for_student),
    path('teacher/getquiz', get_single_quiz_for_teacher),
    path('student/getquiz', get_single_quiz_for_student),
    path('teacher/tasklists', get_tasklists_for_teacher),
    path('student/tasklists', get_tasklists_for_student),
    path('save/tasklist', save_tasklist),
    path('teacher/remove/tasklist', remove_tasklist_for_teacher),
    path('student/remove/tasklist', remove_tasklist_for_student),
    path('teacher/gettasklist', get_single_tasklist_for_teacher),
    path('student/gettasklist', get_single_tasklist_for_student),
    path('teacher/updatetasklist', update_tasklist_for_teacher),
    path('student/updatetasklist', update_tasklist_for_student),
    path('teacher/getStudents', get_students),
    path('student/getTeachers', get_teachers),
    path('teacher/addStudents', add_students),
]

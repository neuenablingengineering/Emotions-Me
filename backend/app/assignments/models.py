from django.db import models
from django.conf import settings


class Assignment(models.Model):

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignment_teacher")
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assignment_list_of_students")  # ['student1', 'student2', 'student3', etc]
    quizName = models.CharField(max_length=100, unique=True)
    quizData = models.TextField()

    def get_assignment(self):
        return self


class Tasklist(models.Model):

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasklist_teacher")
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasklist_list_of_students")  # ['student1', 'student2', 'student3', etc]
    tasklistName = models.CharField(max_length=100, unique=True)
    tasklistData = models.TextField()

    def get_tasklist(self):
        return self

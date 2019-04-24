from rest_framework import serializers
from .models import Assignment, Tasklist


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = '__all__'


class TasklistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasklist
        fields = '__all__'

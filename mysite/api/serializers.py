# api/serializers.py

from rest_framework import serializers
from task.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'desc', 'tag', 'is_priority', 'is_done', 'timestamp']

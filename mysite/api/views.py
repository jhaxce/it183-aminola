# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .serializers import TaskSerializer
from task.models import Task

# Task List (GET), Create Task (POST)
class TaskListCreate(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign the logged-in user to the task
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Task Detail (GET, PUT, DELETE)
class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, task_id, user):
        try:
            return Task.objects.get(id=task_id, user=user)
        except Task.DoesNotExist:
            return None
    
    def get(self, request, task_id):
        task = self.get_object(task_id, request.user)
        if task is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, task_id):
        task = self.get_object(task_id, request.user)
        if task is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id):
        task = self.get_object(task_id, request.user)
        if task is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# api/urls.py

from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token'),
    path('tasks/', views.TaskListCreate.as_view(), name='task_list_create'),
    path('tasks/<int:task_id>/', views.TaskDetail.as_view(), name='task_detail'),
]
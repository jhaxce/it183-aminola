from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('tos/', views.tos, name='tos'),
    path('cookie/', views.cookie, name='cookie'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('account/', views.account_view, name='account'),
    path('account/update_username/', views.update_username, name='update_username'),
    path('account/update_password/', views.update_password, name='update_password'),
    path('account/regenerate_token/', views.regenerate_token, name='regenerate_token'),
    path('logout/', views.user_logout, name='logout'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_form, name='add_task'),
    path('tasks/<int:task_id>/edit/', views.task_form, name='edit_task'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/pin/', views.update_task, name='pin_task'),
    path('tasks/<int:task_id>/unpin/', views.update_task, name='unpin_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/delete/completed/', views.delete_completed_tasks, name='delete_completed_tasks'),
]
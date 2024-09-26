# from django.urls import path
# from .views import blog_list, blog_detail, blog_delete

# urlpatterns = [
#     path('', blog_list),
#     path('<id>/', blog_detail),
#     path('<id>/delete/', blog_delete),
# ]

from django.urls import path
from .views import blog_list, blog_create, blog_update, blog_delete

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('post/new/', blog_create, name='blog_create'),
    path('post/<int:pk>/edit/', blog_update, name='blog_update'),
    path('post/<int:pk>/delete/', blog_delete, name='blog_delete'),
]

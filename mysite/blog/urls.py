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
    path('', blog_list),
    path('post/new/', blog_create),
    # path('post/<id>/', blog_detail),
    path('post/<id>/edit/', blog_update),
    path('post/<id>/delete/', blog_delete),
]

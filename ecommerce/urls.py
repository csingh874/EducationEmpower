from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("courses", views.course_page, name="courses"),
    path("courses/<course_idx>", views.view_course, name="course_details"),
    path("user-login", views.user_login, name="user_login"),
    path("user-logout", views.user_logout, name="user_logout"),
    path("signup", views.user_creation, name="sign_up"),
]

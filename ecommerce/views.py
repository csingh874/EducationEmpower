from django.shortcuts import render
from .models import *
# Create your views here.


# Function to render to the home page and display courses
def home_page(request):
    course_data = CourseDescription.objects.all()
    return render(request, "home.html", {"course_data": course_data})


# Function will display the courses on course page
def course_page(request):
    course_data = CourseDescription.objects.all()
    return render(request, "courses.html", {"course_data": course_data})


def view_course(request, course_idx):
    course_detail = CourseDescription.objects.get(idx=course_idx)
    return render(request, "view_course.html", {"course_detail": course_detail})

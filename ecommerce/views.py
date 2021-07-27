from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, "home.html")


def course_page(request):
    return render(request, "courses.html")

def view_course(request):
    return render(request, "view_course.html")
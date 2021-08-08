from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
# Create your views here.


# Function to render to the home page and display courses
def home_page(request):
    course_data = CourseDescription.objects.all()
    return render(request, "home.html", {"course_data": course_data})


# Function will display the courses on course page
def course_page(request):
    course_data = CourseDescription.objects.all()
    return render(request, "courses.html", {"course_data": course_data})


# View Single Course Detail
def view_course(request, course_idx):
    course_detail = CourseDescription.objects.get(idx=course_idx)
    return render(request, "view_course.html", {"course_detail": course_detail})


# login
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({"data": "success"})
            else:
                return JsonResponse({'data': 'Your Account is Inactive.'})
        else:
            return JsonResponse({'data': 'Incorrect Username or password.'})
    return redirect('home')


# logout
def user_logout(request):
    logout(request)
    return redirect('home')


# user creation
def user_creation(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password1": request.POST.get("password"),
            "password2": request.POST.get("username"),
        }
        form = CustomUserCreationForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        print(form.errors.as_json())
        return JsonResponse(form.errors.as_json(), safe=False)
    return redirect('home')

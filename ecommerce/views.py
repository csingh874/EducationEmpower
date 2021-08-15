from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import SetPasswordForm
from asgiref.sync import sync_to_async
from django.core.mail import send_mail
import pyotp
import base64
import asyncio
from django.conf import settings


# Create your views here.

async def send_otp_mail(sub, msg):
    a_send_mail = sync_to_async(send_mail)
    await a_send_mail(sub, msg, settings.EMAIL_HOST_USER, ['csingh874@gmail.com'], fail_silently=False)


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
            "password2": request.POST.get("confirm_password"),
        }
        form = CustomUserCreationForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse(form.errors.as_json(), safe=False)
    return redirect('home')


# Password Forgot Reset Form
async def password_forgot_reset(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            await sync_to_async(User.objects.get)(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({"error": f"Username {username} does not exist"})
        key = base64.b32encode(bytes(username, encoding='utf-8'))
        totp = pyotp.TOTP(key, interval=300, name=username)
        sub = "Password reset otp."
        msg = f"Hi\n Your otp is {totp.now()}."
        asyncio.create_task(send_otp_mail(sub, msg))
        return JsonResponse({"data": "Success", "key": key.decode('ascii')})
    return redirect("home")


def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        key = request.POST.get('otp_key')
        decode_key = base64.b32decode(key).decode('utf-8')
        totp = pyotp.TOTP(key, interval=300, name=decode_key)
        if totp.verify(otp) is False:
            return JsonResponse({"otp": {"otp_num": [{"message": "Invalid otp number."}]}})
        data = {
            "new_password1": request.POST.get('new_password1'),
            "new_password2": request.POST.get('new_password2'),
        }
        user = User.objects.get(username=decode_key)
        form = SetPasswordForm(data=data, user=user)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": "Password reset successfully"})
        return JsonResponse({"error": form.errors.as_json()})
    return redirect("home")


def my_profile(request):
    return render(request, "profile.html")

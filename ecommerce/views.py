import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from asgiref.sync import sync_to_async
from django.core.mail import send_mail
import pyotp
import base64
import asyncio
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import razorpay
import hmac
import hashlib
from json import loads


# Create your views here.
def razorpay_auth():
    return razorpay.Client(auth=("rzp_test_Jpnr55OprKlG0k", "1kzUy3rpnA0D7DFyUENBYS6j"))


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
    return render(request, "view_course.html", {"course_detail": course_detail, "course_idx": course_idx})


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


@login_required(login_url="home")
def my_profile(request):
    if request.method == "POST":
        data = {
            "first_name": request.POST.get("f_name"),
            "last_name": request.POST.get("l_name"),
            "email": request.POST.get("txt_email"),
        }
        form = UserForm(data, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("my_profile")
    return render(request, "profile.html")


@login_required(login_url="home")
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_profile")
    return render(request, "password_change.html", {"form": form})


@login_required(login_url="home")
def create_razorpay_order(request):
    if request.method == "POST":
        client = razorpay_auth()
        course_idx = request.POST.get('course_idx')
        course = CourseDescription.objects.get(idx=course_idx)
        order_amount = (course.price * 100)
        order_currency = 'INR'
        try:
            obj_order = OrderDetails.objects.get(course_id=course, user_id=request.user, status='created',
                                                 resp__amount=order_amount).resp
        except ObjectDoesNotExist:
            obj_order = client.order.create({'amount': order_amount, 'currency': order_currency})
            new_order = OrderDetails(course_id=course, user_id=request.user, resp=obj_order, status='created')
            new_order.save()
        return JsonResponse({"resp": {"success": obj_order}})
    return redirect("home")


@login_required(login_url='home')
def confirm_payment(request):
    if request.method == 'POST':
        checkout_resp = loads(request.POST.get('data'))
        order_id = request.POST.get('order_id')
        signature = hmac.new(b'1kzUy3rpnA0D7DFyUENBYS6j', f'{order_id}|{checkout_resp.get("razorpay_payment_id")}'.
                             encode(), hashlib.sha256).hexdigest()
        if signature == checkout_resp.get("razorpay_signature"):
            ord_detail = OrderDetails.objects.get(user_id=request.user, resp__id=order_id)
            ord_detail.status, ord_detail.checkout_resp = 'success', checkout_resp
            ord_detail.save()
            return JsonResponse({"success": "success"})
    return redirect('home')


@login_required()
def new_home(request):
    return render(request, "new_home.html")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from .models import UserProfile
import random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import base64
def signup(request):
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            if user_profile.user_type == 'patient':
                return redirect('patient')
            elif user_profile.user_type == 'doctor':
                return redirect('doctor')
        except:
            return redirect('login')

    if request.method == "POST":
        emaill=request.POST.get('email')

        try:
            User.objects.get(email=emaill)
            messages.error(request,'Email alredy exist')
            return redirect('signup')
        except:

            data = {
                'first_name': request.POST.get("first_name"),
                'last_name': request.POST.get("last_name"),
                'username': request.POST.get("username"),
                'email': request.POST.get("email"),
                'password': request.POST.get("password"),
                'confirm_password': request.POST.get("confirm_password"),
                'user_type': request.POST.get("user_type"),
                'address': request.POST.get("address_line1"),
                'state': request.POST.get("state"),
                'city': request.POST.get("city"),
                'pincode': request.POST.get("pincode"),
            }
            avatar = request.FILES.get("profile_picture")

            if User.objects.filter(email=data['email']).exists():
                messages.error(request, "Email already exists")
                return render(request, "signup.html")
            if data['password'] != data['confirm_password']:
                return render(request, "signup.html")

            request.session['signup_data'] = data

            import base64
            request.session['avatar'] = base64.b64encode(avatar.read()).decode('utf-8')
            request.session['avatar_name'] = avatar.name

            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp

            send_mail(
                'Your OTP for Signup Verification',
                f'Your OTP is: {otp}',
                "your@email.com",
                [data['email']],
                fail_silently=False,
            )
            return redirect('verify_otp')
    return render(request, "signup.html")

from django.core.files.base import ContentFile






def verify_otp(request):
    data = request.session.get("signup_data")
    username = "xxxxxx"
    email = "xxxxxx"
    actual_otp = request.session.get("otp")


    if not actual_otp:
        return redirect('signup')
    

    if data:
            username = data.get('username','xxxxxx')
            email = data.get('email','xxxxxx')
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        
        
        avatar_data = request.session.get("avatar")
        avatar_name = request.session.get("avatar_name")

        

        if entered_otp == actual_otp and data and avatar_data:
            avatar_file = ContentFile(base64.b64decode(avatar_data), name=avatar_name)

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password']
            )

            UserProfile.objects.create(
                user=user,
                user_type=data['user_type'],
                profile_picture=avatar_file,
                address_line1=data['address'],
                city=data['city'],
                state=data['state'],
                pincode=data['pincode']
            )

            request.session.flush()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP")
    return render(request, "verify_otp.html", {'username': username, 'email': email})









def login(request):
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            if user_profile.user_type == 'patient':
                return redirect('patient')
            elif user_profile.user_type == 'doctor':
                return redirect('doctor')
        except:
            return redirect('login')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email")
            return render(request, 'login.html')

        user_auth = authenticate(request, username=user.email, password=password)
        if user_auth is not None:
            profile = UserProfile.objects.get(user=user_auth)
            if profile.user_type == user_type:
                auth_login(request, user_auth)
                if user_type == 'patient':
                    return redirect('patient') 
                else:
                    return redirect('doctor') 
            else:
                messages.error(request, "User type mismatch")
        else:
            messages.error(request, "Incorrect Password")
    return render(request, 'login.html')




def home(request):
    return render(request,'home.html')






@login_required
def patient(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.user_type != 'patient':
        return redirect('doctor')  
    username=request.user.username
    return render(request, 'patient.html',{'username':username})





@login_required
def doctor(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.user_type != 'doctor':
        return redirect('patient')
    username = request.user.username
    return render(request, 'doctor.html', {'username': username})




def logoutt(request):
    logout(request)
    return redirect('login')





from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('doctor/', views.doctor, name='doctor'),
    path('patients/', views.patient, name='patient'),
    path('logout/', views.logoutt, name='logout'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
]
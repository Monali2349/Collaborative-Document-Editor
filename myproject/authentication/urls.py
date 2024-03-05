from django.urls import path,include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # path("", views.dashboard, name="dashboard"),
    path('',include('dashboard.urls')),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('register/',views.register,name="register"),
    path('send_otp/',views.send_otp,name="send_otp"),
    path('forget/',views.forget_password,name='forget'),
    path('reset_otp',views.reset_otp,name='reset_otp'),
]

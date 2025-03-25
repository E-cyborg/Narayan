from django.contrib import admin
from django.urls import path
from register import views

urlpatterns = [
    path("sign",views.Registration,name="sign"),
    path("login",views.loginUser,name="login"),
    path("user", views.user_dashboard, name="user_dashboard"),
    path("logout",views.logout_user,name="logout")
]

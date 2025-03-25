from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import login_form, RegisterForm



def User_sign(req):
    return render(req,"sign.html",{})


def loginUser(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('/')
    form = login_form()
    if request.method == "POST":
        form = login_form(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data["email_or_username"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(email=email_or_username).first()
            if user:
                user = authenticate(request, username=user.username, password=password)
            else:
                user = authenticate(request, username=email_or_username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('/')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return redirect('login')
    return render(request, "login.html", {"form": form})


def logout_user(request):
    messages.success(request, "Logged out.")
    logout(request)
    return redirect("/")



def user_dashboard(request):
    if request.user.is_authenticated:
        return render(request, "user.html", {"user": request.user})
    else:
        messages.info(request, "You are not logged in.")
        return redirect('login')

def Registration(req):
    form = RegisterForm(req.POST or None)  # Initialize with POST data if available
    
    if req.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            if User.objects.filter(email=email).exists():
                messages.error(req, 'Email already exists. Please log in.')
                return redirect('login')  # Redirects to login page if email exists

            form.save()  # Saves user with hashed password
            messages.success(req, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect after successful registration
    
    return render(req, "sign.html", {"form": form})  # Renders form if GET request
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm
from employees.models import EmployeeProfile # Make sure this import is here
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            EmployeeProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
        else:
            # THIS WILL PRINT THE ERRORS TO YOUR CONSOLE/TERMINAL
            print("Form is not valid. Errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})
# Assuming you have a register.html

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! 👋")

            # ✅ Smart redirection logic
            next_page = request.GET.get("next") or request.POST.get("next")
            if next_page == "home":
                return redirect("home")  # Redirect back to home if came from Request Demo
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out. 👋")
    return redirect("home")
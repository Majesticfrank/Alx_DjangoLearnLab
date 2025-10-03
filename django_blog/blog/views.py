from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, "home.html")

def signup_view(request):
    if request.method == 'POST':
        form =SignupForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request, user)
            return redirect("login")
    else:

            form=SignupForm()
    return render(request, "register.html", {"form":form})
    
def login_view(request):
  if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            # wrong credentials → show error
            return render(request, "login.html", {"error": "Invalid credentials"})
    
    # GET request → just show the form
  return render(request, "login.html")
    

@login_required
def profile_view(request):
    if request.method =="POST":
        request.user.email =request.POST.get("email")
        request.user.save()
        return redirect("profile")
    return render(request,"profile.html", {"user":request.user})
    
def logout_view(request):
    logout(request)
    return redirect("login")


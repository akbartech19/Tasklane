from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.models import User

def register_user(request):
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        email = request.POST.get("email")

        new_user = User.objects.create_user(
            first_name = full_name.split(" ")[0].strip(),
            last_name = full_name.split(" ")[1].strip(),
            password = password,
            email = email,
            username = email
        )
        return redirect("accounts_app:login")


    return render(request, "register.html")



def login_user(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")


        user = authenticate(username=email, password = password)
        if user is None:
            messages.error(request, "Username or password is invalid !")
            return redirect("accounts_app:login")

        login(request, user)
        return redirect("task:home")


    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts_app:login")
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


def login_view(request):
    return render(request, "users/signup.html")


def signup(request):
    """User registration view."""
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form = UserCreationForm(request.POST)
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("login")
    return render(request, "users/signup.html", {"form": form})

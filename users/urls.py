from django.urls import path

from .views import login_view, signup

urlpatterns = [
    path("/signup", signup, name="signup"),
    path("", login_view, name="login"),
]

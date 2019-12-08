"""Users authentication testcases"""
import pytest

from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from model_bakery import baker


def test_signup_get_request(client):
    """On GET request, a 200 status code is responded."""
    response = client.get(reverse("signup"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_user_creation(client):
    """
    On succesful POST request, a User should be created and the user should
     be authenticated.
    """
    assert User.objects.count() == 0
    client.post(
        reverse("signup"),
        {"username": "eric", "password1": "centipad", "password2": "centipad"},
    )
    assert User.objects.count() == 1
    user = auth.get_user(client)
    assert user.is_authenticated


@pytest.mark.django_db
def test_signup_fail(client):
    """
    On unsuccesful POST request, a User should not be created and the user
     should not be authenticated.
    """
    assert User.objects.count() == 0
    client.post(
        reverse("signup"),
        {"username": "eric", "password1": "centipad", "password2": "2312"},
    )
    assert User.objects.count() == 0
    user = auth.get_user(client)
    assert not user.is_authenticated


def test_login_get_request(client):
    """On login GET request, a 200 status code is responded."""
    response = client.get(reverse("login"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_succesful(client):
    """On successful login POST request, the user should be authenticated."""
    u = baker.make("User", username="eric")
    u.set_password("coonnfriends")
    u.save()
    response = client.post(
        reverse("login"), {"username": "eric", "password": "coonnfriends"}
    )
    u = User.objects.get()
    user = auth.get_user(client)
    assert response.status_code == 302
    assert user.is_authenticated


@pytest.mark.django_db
def test_login_fail(client):
    """On failed login request, the user should not be authenticated."""
    u = baker.make("User", username="eric")
    u.set_password("coonnfriends")
    u.save()
    response = client.post(
        reverse("login"), {"username": "eric", "password": "wrongpass"}
    )
    u = User.objects.get()
    user = auth.get_user(client)
    assert response.status_code == 200
    assert not user.is_authenticated

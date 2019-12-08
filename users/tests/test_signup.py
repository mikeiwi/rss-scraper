"""Users signup testcases"""
import pytest

from django.contrib import auth
from django.contrib.auth.models import User


def test_signup_get_request(client):
    """On GET request, a 200 status code is responded."""
    response = client.get("")
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_user_creation(client):
    """
    On succesful POST request, a User should be created and the user should
     be authenticated.
    """
    assert User.objects.count() == 0
    client.post(
        "", {"username": "eric", "password1": "centipad", "password2": "centipad"}
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
        "", {"username": "eric", "password1": "centipad", "password2": "2312"}
    )
    assert User.objects.count() == 0
    user = auth.get_user(client)
    assert not user.is_authenticated

"""Users authentication testcases"""
from django.urls import reverse


def test_unauthenticated_user(client):
    """An unauthenticated user should be redirected to the login page."""
    response = client.get(reverse("user_feed_list"))
    assert response.status_code == 302
    assert "/login" in response["location"]

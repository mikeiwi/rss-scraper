"""Users authentication testcases"""
import pytest
from django.urls import reverse

from model_bakery import baker


def test_unauthenticated_user(client):
    """An unauthenticated user should be redirected to the login page."""
    response = client.get(reverse("user_feed_list"))
    assert response.status_code == 302
    assert "/login" in response["location"]


@pytest.mark.django_db
def test_subscribed_feeds(client):
    """The feed list may only contain feeds which the user is subscribed to."""
    u = baker.make("User", username="eric")
    u.set_password("coonnfriends")
    u.save()

    baker.make("Feed", title="My awesome feed", users=[u])
    baker.make("Feed", title="Another cool one", users=[u])
    baker.make("Feed", title="This is lame, but gives me a moral superiority")

    client.login(username="eric", password="coonnfriends")
    response = client.get(reverse("user_feed_list"))
    assert response.status_code == 200
    assert response.content.count(b"<li>") == 2

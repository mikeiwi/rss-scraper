"""Feed list testcases"""
import pytest
from django.urls import reverse

from model_bakery import baker


def test_unauthenticated_user(client):
    """An unauthenticated user should be redirected to the login page."""
    response = client.get(reverse("user_feed_list"))
    assert response.status_code == 302
    assert "/login" in response["location"]


@pytest.mark.django_db
def test_subscribed_feeds(client, authenticated_user):
    """The feed list may only contain feeds which the user is subscribed to."""
    baker.make("Feed", title="My awesome feed", users=[authenticated_user])
    baker.make("Feed", title="Another cool one", users=[authenticated_user])
    baker.make("Feed", title="This is lame, but gives me moral superiority")

    response = client.get(reverse("user_feed_list"))
    assert response.status_code == 200
    assert response.content.count(b"<li>") == 2

"""Feed list testcases"""
import pytest
from django.urls import reverse
from model_bakery import baker

from feeds.models import Feed


@pytest.mark.django_db
def test_create_feed(client):
    """Feed creation should be successfuly saved and with the user set."""
    u = baker.make("User", username="eric")
    u.set_password("coonnfriends")
    u.save()

    client.login(username="eric", password="coonnfriends")
    assert Feed.objects.count() == 0
    client.post(
        reverse("user_feed_create"),
        {"url": "https://my-grandma-flirting-lessons-blog.me/rss"},
    )
    assert Feed.objects.count() == 1
    feed = Feed.objects.get()
    assert feed.users.filter(id=u.id).exists()

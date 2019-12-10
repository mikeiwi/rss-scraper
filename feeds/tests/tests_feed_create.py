"""Feed create testcases"""
import pytest
from django.urls import reverse
from model_bakery import baker

from feeds.models import Feed


@pytest.mark.django_db
def test_create_feed_view(client, authenticated_user):
    """Feed creation view GET request should respond successfuly."""
    response = client.get(reverse("user_feed_follow"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_feed(client, authenticated_user):
    """Feed creation should be successfuly saved and with the user set."""
    assert Feed.objects.count() == 0
    client.post(
        reverse("user_feed_follow"),
        {"url": "https://my-grandma-flirting-lessons-blog.me/rss"},
    )
    assert Feed.objects.count() == 1
    feed = Feed.objects.get()
    assert feed.users.filter(id=authenticated_user.id).exists()


@pytest.mark.django_db
def test_follow_existing_feed(client, authenticated_user):
    """Attempting to create an existing feed shouldn't create a new one."""
    baker.make("Feed", url="https://my-grandma-flirting-lessons-blog.me/rss")
    client.post(
        reverse("user_feed_follow"),
        {"url": "https://my-grandma-flirting-lessons-blog.me/rss"},
    )
    assert Feed.objects.count() == 1
    feed = Feed.objects.get()
    assert feed.users.filter(id=authenticated_user.id).exists()

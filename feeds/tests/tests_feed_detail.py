"""Feed entries testcases"""
import pytest
from django.urls import reverse

from model_bakery import baker


@pytest.mark.django_db
def test_entries_list(client, authenticated_user):
    """A feed page should list all of its entries."""
    feed = baker.make("Feed")
    baker.make("Entry", feed=feed, _quantity=18)
    baker.make("Entry", _quantity=10)
    response = client.get(reverse("feed_entries", kwargs={"feed_id": feed.id}))
    assert response.status_code == 200
    assert response.content.count(b"<li>") == 18


@pytest.mark.django_db
def test_bookmark_entry(client, authenticated_user):
    """A user may bookmark an Entry in any feed."""
    entry = baker.make("Entry")
    response = client.post(reverse("bookmark_entry", kwargs={"entry_id": entry.id}))
    assert response.status_code == 200
    assert entry.bookmarks.filter(id=authenticated_user.id).exists()


@pytest.mark.django_db
def test_bookmark_unexisting_entry(client, authenticated_user):
    """if an entry does not exists, an error is responded."""
    response = client.post(reverse("bookmark_entry", kwargs={"entry_id": 123}))
    assert response.status_code == 404

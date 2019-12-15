"""Testcases for mass feed updating task"""
import pytest
from model_bakery import baker

from feeds.tasks import update_all_feeds


@pytest.mark.django_db
def test_update_all_feeds(mocker):
    """When calling massiva update feed function, all feeds are updated."""
    m = mocker.patch("feeds.tasks.update_feed")
    baker.make("Feed", _quantity=10)
    update_all_feeds()
    assert m.call_count == 10

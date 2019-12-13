"""Testcases for feed updating task"""
import pytest
from model_bakery import baker

from feeds.tasks import update_feed


@pytest.mark.django_db
def test_feedparser_called(mocker):
    """Feed updating should call feedparser"""
    m = mocker.patch("feedparser.parse")
    feed = baker.make("Feed", url="https://hannibal-cooking-course.info/rss")
    update_feed(feed.id)
    m.assert_called_with("https://hannibal-cooking-course.info/rss")

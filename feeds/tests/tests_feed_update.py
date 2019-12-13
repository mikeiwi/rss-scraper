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


@pytest.mark.django_db
def test_parsed_entries(mocker, feedparser_data):
    """Parsed info and entries should be inserted in DB."""
    m = mocker.patch("feedparser.parse")
    m.return_value = feedparser_data
    feed = baker.make("Feed")
    update_feed(feed.id)
    assert feed.entry_set.count() == 3

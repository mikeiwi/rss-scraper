"""Testcases for feed updating task"""
import pytest
from model_bakery import baker

from feeds.tasks import update_feed


@pytest.mark.django_db
def test_feedparser_called(mocker, feedparser_data):
    """Feed updating should call feedparser"""
    m = mocker.patch("feedparser.parse")
    m.return_value = feedparser_data
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


@pytest.mark.django_db
def test_parsed_entries_update(mocker, feedparser_data):
    """Parsed info and entries should be inserted in DB, unless they already exist."""
    m = mocker.patch("feedparser.parse")
    m.return_value = feedparser_data
    feed = baker.make("Feed")
    baker.make("Entry", feed=feed, link=feedparser_data["entries"][0]["link"])
    update_feed(feed.id)
    assert feed.entry_set.count() == 3


@pytest.mark.django_db
def test_gone_feed(mocker):
    """When a feed is parsed with 410 status, it should be set as gone"""
    m = mocker.patch("feedparser.parse")
    m.return_value = {"status": 410}
    feed = baker.make("Feed")
    update_feed(feed.id)
    feed.refresh_from_db()
    assert feed.gone is True


@pytest.mark.django_db
@pytest.mark.parametrize(
    "feedparser_test_data",
    [
        {"status": 404, "bozo": 0},
        {"status": 500, "bozo": 0},
        {"status": 200, "bozo": 1},
    ],
)
def test_parsing_fail(mocker, feedparser_test_data):
    """
    When parsing fails somehow (failed request or malformed rss), 1 is added to
    a counter for failed_tries.
    """
    m = mocker.patch("feedparser.parse")
    m.return_value = feedparser_test_data
    feed = baker.make("Feed")
    update_feed(feed.id)
    feed.refresh_from_db()
    assert feed.failed_tries == 1


@pytest.mark.django_db
def test_reset_failed_tries(mocker, feedparser_data):
    """On succesful parse, `failed_tries` counter should be reset."""
    m = mocker.patch("feedparser.parse")
    m.return_value = feedparser_data
    feed = baker.make("Feed", failed_tries=42)
    update_feed(feed.id)
    feed.refresh_from_db()
    assert feed.failed_tries == 0

"""Testcases for feed updating task"""
import pytest
from django.urls import reverse
from model_bakery import baker

from feeds.tasks import update_feed


@pytest.fixture
def test_feed():
    """Creates a fresh baked Feed instance."""
    return baker.make("Feed", url="https://my-grandma-frilrting-lessons/rss")


@pytest.fixture
def feedparser_mock(mocker, feedparser_data):
    """Mocks feedparser library and returns some fixture data."""
    m = mocker.patch("feedparser.parse")
    m.return_value = feedparser_data
    return m


@pytest.mark.django_db
def test_feedparser_called(feedparser_mock, test_feed):
    """Feed updating should call feedparser and insert entries in DB"""
    update_feed(test_feed.id)
    feedparser_mock.assert_called_with(test_feed.url)
    assert test_feed.entry_set.count() == 3


@pytest.mark.django_db
def test_parsed_entries_update(feedparser_mock, test_feed, feedparser_data):
    """Parsed info and entries should be inserted in DB, unless they already exist."""
    baker.make("Entry", feed=test_feed, link=feedparser_data["entries"][0]["link"])
    update_feed(test_feed.id)
    assert test_feed.entry_set.count() == 3


@pytest.mark.django_db
def test_gone_feed(feedparser_mock, test_feed):
    """When a feed is parsed with 410 status, it should be set as gone"""
    feedparser_mock.return_value = {"status": 410}
    update_feed(test_feed.id)
    test_feed.refresh_from_db()
    assert test_feed.gone is True


@pytest.mark.django_db
@pytest.mark.parametrize(
    "feedparser_test_data",
    [
        {"status": 404, "bozo": 0},
        {"status": 500, "bozo": 0},
        {"status": 200, "bozo": 1},
    ],
)
def test_parsing_fail(feedparser_mock, test_feed, feedparser_test_data):
    """
    When parsing fails somehow (failed request or malformed rss), 1 is added to
    a counter for failed_tries.
    """
    feedparser_mock.return_value = feedparser_test_data
    update_feed(test_feed.id)
    test_feed.refresh_from_db()
    assert test_feed.failed_tries == 1


@pytest.mark.django_db
def test_reset_failed_tries(feedparser_mock, feedparser_data):
    """On succesful parse, `failed_tries` counter should be reset."""
    feed = baker.make("Feed", failed_tries=42)
    update_feed(feed.id)
    feed.refresh_from_db()
    assert feed.failed_tries == 0


@pytest.mark.django_db
def test_update_manual(client, authenticated_user, mocker, test_feed):
    """Updating a feed manually should call the update feed task."""
    m = mocker.patch("feeds.views.update_feed")
    client.post(reverse("user_update_feed", kwargs={"feed_id": test_feed.id}))
    assert m.delay.called

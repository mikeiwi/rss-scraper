import feedparser

from feeds.models import Feed


def update_feed(feed_id):
    feed = Feed.objects.get(id=feed_id)
    feedparser.parse(feed.url)

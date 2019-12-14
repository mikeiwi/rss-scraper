import feedparser

from feeds.models import Feed, Entry


def update_feed(feed_id):
    feed = Feed.objects.get(id=feed_id)
    d = feedparser.parse(feed.url)
    for entry in d["entries"]:
        Entry.objects.update_or_create(
            link=entry["link"],
            defaults={
                "feed": feed,
                "title": entry["title"],
                "summary": entry["summary"],
                "content": entry["content"],
            },
        )

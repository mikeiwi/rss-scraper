import feedparser
from celery.utils.log import get_task_logger
from config.celery import app
from django.conf import settings

from feeds.models import Feed, Entry

logger = get_task_logger(__name__)


@app.task
def update_feed(feed_id):
    """Updates a single feed

    Parameters:
    -----------
    feed_id : int
        The id of the feed to be updated.
    """
    feed = Feed.objects.get(id=feed_id)
    d = feedparser.parse(feed.url)

    if d["status"] == 410:
        feed.gone = True
        feed.save()
        return

    if d["status"] > 400 or d["bozo"] == 1:
        feed.failed_tries += 1
        feed.save()
        return

    feed.failed_tries = 0
    feed.save()
    for entry in d["entries"]:
        Entry.objects.update_or_create(
            link=entry["link"],
            defaults={
                "feed": feed,
                "title": entry["title"],
                "summary": entry["summary"],
            },
        )


@app.task
def update_all_feeds():
    """Update all feeds in the system"""
    logger.info('Updating all existing feeds!')
    for feed in Feed.objects.filter(
        gone=False, failed_tries__lte=settings.MAX_FAILED_TRIES
    ):
        update_feed(feed.id)

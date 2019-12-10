from django.urls import path

from .views import FeedListView, FeedEntriesListView
from .views import bookmark_entry, follow_feed

urlpatterns = [
    path("/list", FeedListView.as_view(), name="user_feed_list"),
    path("/follow", follow_feed, name="user_feed_follow"),
    path("/<int:feed_id>", FeedEntriesListView.as_view(), name="feed_entries"),
    path("/bookmark/<int:entry_id>", bookmark_entry, name="bookmark_entry"),
]

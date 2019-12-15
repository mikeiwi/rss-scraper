from django.urls import path

from .views import FeedListView, FeedEntriesListView, BookmarkListView
from .views import bookmark_entry, follow_feed, user_update_feed

urlpatterns = [
    path("", FeedListView.as_view(), name="user_feed_list"),
    path("follow", follow_feed, name="user_feed_follow"),
    path("<int:feed_id>", FeedEntriesListView.as_view(), name="feed_entries"),
    path("bookmark/<int:entry_id>", bookmark_entry, name="bookmark_entry"),
    path("bookmark", BookmarkListView.as_view(), name="bookmark_list"),
    path("update/<int:feed_id>", user_update_feed, name="user_update_feed"),
]

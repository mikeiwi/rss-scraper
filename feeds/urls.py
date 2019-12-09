from django.urls import path

from .views import FeedListView, FeedCreateView, FeedEntriesListView

urlpatterns = [
    path("/list", FeedListView.as_view(), name="user_feed_list"),
    path("/create", FeedCreateView.as_view(), name="user_feed_create"),
    path("/<int:feed_id>", FeedEntriesListView.as_view(), name="feed_entries"),
]

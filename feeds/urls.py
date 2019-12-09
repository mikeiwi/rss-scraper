from django.urls import path

from .views import FeedListView, FeedCreateView

urlpatterns = [
    path("/list", FeedListView.as_view(), name="user_feed_list"),
    path("/create", FeedCreateView.as_view(), name="user_feed_create"),
]

from django.urls import path

from .views import FeedListView

urlpatterns = [path("/list", FeedListView.as_view(), name="user_feed_list")]

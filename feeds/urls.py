from django.urls import path

from .views import feed_list

urlpatterns = [path("/list", feed_list, name="user_feed_list")]

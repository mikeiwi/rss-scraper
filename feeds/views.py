from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import Feed


class FeedListView(LoginRequiredMixin, ListView):
    model = Feed

    def get_queryset(self):
        queryset = Feed.objects.filter(users=self.request.user)
        return queryset


class FeedCreateView(LoginRequiredMixin, CreateView):
    model = Feed
    fields = ["url"]
    success_url = reverse_lazy("user_feed_list")

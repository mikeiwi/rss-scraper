from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Feed


class FeedListView(LoginRequiredMixin, ListView):
    model = Feed

    def get_queryset(self):
        queryset = Feed.objects.filter(users=self.request.user)
        return queryset

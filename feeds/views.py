from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Feed


class FeedListView(LoginRequiredMixin, ListView):
    model = Feed

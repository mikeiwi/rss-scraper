from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Feed, Entry


class FeedListView(LoginRequiredMixin, ListView):
    model = Feed

    def get_queryset(self):
        queryset = Feed.objects.filter(users=self.request.user)
        return queryset


class FeedCreateView(LoginRequiredMixin, CreateView):
    model = Feed
    fields = ["url"]
    success_url = reverse_lazy("user_feed_list")

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        form.instance.users.add(self.request.user)
        form.instance.save()
        return form_valid


class FeedEntriesListView(LoginRequiredMixin, ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(feed_id=self.kwargs['feed_id'])


def bookmark_entry(request, entry_id):
    """Set an entry as favourite for the user."""
    entry = get_object_or_404(Entry, id=entry_id)
    entry.bookmarks.add(request.user)
    return render(request, "feeds/bookmark_entry.html")

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from .forms import FollowFeedForm
from .models import Feed, Entry
from .tasks import update_feed


class FeedListView(LoginRequiredMixin, ListView):
    model = Feed

    def get_queryset(self):
        queryset = Feed.objects.filter(users=self.request.user)
        return queryset


@login_required
def follow_feed(request):
    form = FollowFeedForm()
    if request.method == "POST":
        form = FollowFeedForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get("url")
            feed, _ = Feed.objects.get_or_create(url=url)
            feed.users.add(request.user)
            feed.save()
            return redirect("user_feed_list")

    return render(request, "feeds/feed_follow.html", {"form": form})


class FeedEntriesListView(LoginRequiredMixin, ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(feed_id=self.kwargs["feed_id"])


@login_required
@require_http_methods(["POST"])
def bookmark_entry(request, entry_id):
    """Set an entry as favourite for the user."""
    entry = get_object_or_404(Entry, id=entry_id)
    entry.bookmarks.add(request.user)
    return render(request, "feeds/bookmark_entry.html")


class BookmarkListView(LoginRequiredMixin, ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(bookmarks=self.request.user)


@login_required
@require_http_methods(["POST"])
def user_update_feed(request, feed_id):
    update_feed.delay(feed_id)
    return render(request, "feeds/user_update_feed.html", {"feed_id": feed_id})

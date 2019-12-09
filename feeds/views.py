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

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        form.instance.users.add(self.request.user)
        form.instance.save()
        return form_valid

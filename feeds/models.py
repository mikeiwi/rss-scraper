from django.contrib.auth.models import User
from django.db import models


class Feed(models.Model):
    url = models.CharField("Feed URL", max_length=200)
    title = models.CharField("Feed title", max_length=100, blank=True)
    updated = models.DateTimeField("Feed origin data update date", null=True)
    modified_dt = models.DateTimeField("Internal update date", auto_now=True)
    creation_dt = models.DateTimeField("Creation date", auto_now_add=True)
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ["modified_dt"]

    def __str__(self):
        return self.title


class Entry(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    link = models.CharField("Entry URL", max_length=200)
    title = models.CharField(max_length=100)
    summary = models.TextField()
    content = models.TextField("Complete content")
    updated = models.DateTimeField("Update time according to source")

    class Meta:
        ordering = ["updated"]

    def __str__(self):
        return self.title

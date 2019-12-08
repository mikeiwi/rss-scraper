from django.contrib.auth.models import User
from django.db import models


class Feed(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    updated = models.DateTimeField("Feed data update date")
    modified_dt = models.DateTimeField("Internal update date", auto_now=True)
    creation_dt = models.DateTimeField("Creation date", auto_now_add=True)
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ["modified_dt"]

    def __str__(self):
        return self.title

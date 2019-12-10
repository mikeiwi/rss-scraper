from django import forms
from django.core.validators import URLValidator


class FollowFeedForm(forms.Form):
    url = forms.CharField(label="Feed URL", max_length=200, validators=[URLValidator()])

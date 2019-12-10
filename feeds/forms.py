from django import forms


class FollowFeedForm(forms.Form):
    url = forms.CharField(label='Feed URL', max_length=200)

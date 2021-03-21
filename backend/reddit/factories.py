import factory
from . import models


class SubredditFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Subreddit

    id = "subreddit_id"
    display_name = "subreddit_name"
    title = "subreddit_title"

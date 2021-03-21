import factory
from . import models
from datetime import datetime
from django.utils import timezone


class SubredditFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Subreddit

    id = "subreddit_id"
    display_name = "subreddit_name"
    title = "subreddit_title"


class RedditorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Redditor

    id = "redditor_id"
    name = "redditor_name"


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Submission

    id = "submission_id"
    subreddit = factory.SubFactory(SubredditFactory)
    redditor = factory.SubFactory(RedditorFactory)
    name = "redditor_name"
    karma = 100
    upvote_ratio = 10.10
    num_comments = 50
    created_utc = datetime(2021, 1, 4, tzinfo=timezone.utc)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comment

    id = "comment_id"
    subreddit = factory.SubFactory(SubredditFactory)
    redditor = factory.SubFactory(RedditorFactory)
    submission = factory.SubFactory(SubmissionFactory)
    karma = 100
    created_utc = datetime(2021, 1, 4, tzinfo=timezone.utc)

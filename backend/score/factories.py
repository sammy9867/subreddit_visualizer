import factory
from . import models
from reddit.factories import RedditorFactory, SubredditFactory
from datetime import datetime
from decimal import Decimal
from django.utils import timezone


class WeeklyRedditorScoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WeeklyRedditorScore

    subreddit = factory.SubFactory(SubredditFactory)
    redditor = factory.SubFactory(RedditorFactory)
    score_type = "SUB"
    score = Decimal("1000.10")
    rank = 1
    week_number = datetime(2021, 1, 4, tzinfo=timezone.utc).isocalendar()[1]
    created_utc = datetime(2021, 1, 4, tzinfo=timezone.utc)

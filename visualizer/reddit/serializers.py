from rest_framework import serializers
from .models import Subreddit, WeeklyRedditorScore


class SubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subreddit
        fields = ("id", "display_name", "title")


class WeeklyRedditorScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyRedditorScore
        fields = (
            "subreddit_id",
            "redditor_id",
            "score_type",
            "score",
            "rank",
            "week_number",
            "created_utc",
        )

from rest_framework import serializers
from collector.models import Subreddit

class SubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subreddit
        fields = ('id', 'display_name', 'title')
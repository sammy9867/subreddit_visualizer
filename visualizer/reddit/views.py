from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from .models import Subreddit
from .serializers import SubredditSerializer


class SubredditViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubredditSerializer
    queryset = Subreddit.objects.all()

from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from datetime import timedelta
from django.utils import timezone

from .models import Subreddit, WeeklyRedditorScore
from .serializers import SubredditSerializer, WeeklyRedditorScoreSerializer


class SubredditViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubredditSerializer
    queryset = Subreddit.objects.all()


# http://localhost:8000/api/v1/subreddits/2s3qj/weekly-scores
# http://localhost:8000/api/v1/subreddits/2s3qj/weekly-scores?score_type=sub
class WeeklyRedditorScoreView(ListModelMixin, generics.GenericAPIView):
    serializer_class = WeeklyRedditorScoreSerializer

    def _get_timezone_details(self, now):
        dt = now - timedelta(days=7)
        return dt.isocalendar()[1], dt.year

    def get_queryset(self):
        now = timezone.now()
        week_number, year = self._get_timezone_details(now)
        if week_number is None or year is None:
            return Response(
                {"error": "Something went wrong.."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        queryset = WeeklyRedditorScore.objects.filter(
            subreddit_id=self.kwargs["subreddit_id"],
            week_number=week_number,
            created_utc__year=year,
        )

        score_type = self.request.query_params.get("score_type", None)
        if score_type != None:
            queryset = queryset.filter(score_type=score_type.upper())
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

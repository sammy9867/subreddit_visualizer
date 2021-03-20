from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from score.models import WeeklyRedditorScore
from score.serializers import WeeklyRedditorScoreSerializer

# http://localhost:8000/api/v1/weekly_scores/?score_type=sub&week_number=10&year=2021
# http://localhost:8000/api/v1/weekly_scores/?score_type=com&week_number=10&year=2021&subreddit_id=2s3qj
class WeeklyRedditorScoreViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = WeeklyRedditorScoreSerializer

    def get_queryset(self):
        score_type = self.request.query_params.get("score_type", None)
        week_number = self.request.query_params.get("week_number", None)
        year = self.request.query_params.get("year", None)
        if week_number is None or year is None or score_type is None:
            return Response(
                {"error": "score_type, week_number and year required"},
                status=HTTP_400_BAD_REQUEST,
            )
        queryset = WeeklyRedditorScore.objects.filter(
            score_type=score_type.upper(),
            week_number=week_number,
            created_utc__year=year,
        )
        subreddit_id = self.request.query_params.get("subreddit_id", None)
        if subreddit_id != None:
            queryset = queryset.filter(subreddit_id=subreddit_id)
        return queryset

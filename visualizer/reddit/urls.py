from rest_framework import routers
from django.urls import include, path

from .views import SubredditViewSet, WeeklyRedditorScoreView

router = routers.DefaultRouter()
router.register("", SubredditViewSet, basename="subreddits")

urlpatterns = [
    path(
        "subreddits/",
        include(
            [
                path("", include(router.urls)),
                path(
                    "<str:subreddit_id>/weekly-scores",
                    WeeklyRedditorScoreView.as_view(),
                    name="weekly-scores-list",
                ),
            ]
        ),
    ),
]

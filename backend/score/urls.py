from .views import WeeklyRedditorScoreViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"weekly-scores", WeeklyRedditorScoreViewSet, basename="weekly-scores")

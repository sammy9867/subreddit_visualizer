from .views import SubredditViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"subreddits", SubredditViewSet, basename="subreddits")

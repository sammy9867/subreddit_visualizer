from django.urls import include, path
from reddit.urls import router as reddit_router
from score.urls import router as score_router

urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("", include(reddit_router.urls)),
                path("", include(score_router.urls)),
            ]
        ),
    ),
]

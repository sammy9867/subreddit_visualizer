from django.urls import include, path
from reddit.urls import urlpatterns as reddit_urls

urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("", include(reddit_urls)),
            ]
        ),
    ),
]

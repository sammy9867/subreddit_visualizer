from unittest.mock import patch

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from reddit import models, factories


class SubredditViewSetTest(TestCase):
    def setUp(self):
        self.subreddit = factories.SubredditFactory()
        self.client = APIClient()
        self.url = reverse("subreddits-list")

    def test_subreddits(self):
        response = self.client.get(self.url)
        expected_response = [
            {
                "id": "subreddit_id",
                "display_name": "subreddit_name",
                "title": "subreddit_title",
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)


class WeeklyRedditorScoreViewTest(TestCase):
    def setUp(self):
        week_number = timezone.datetime(
            2020, 12, 30, tzinfo=timezone.utc
        ).isocalendar()[1]
        created_utc = timezone.datetime(2020, 12, 30, tzinfo=timezone.utc)
        self.weekly_score = factories.WeeklyRedditorScoreFactory(
            score_type="SUB", week_number=week_number, created_utc=created_utc
        )
        self.client = APIClient()
        self.url_name = "weekly-scores-list"
        self.url = reverse(self.url_name, kwargs={"subreddit_id": "subreddit_id"})

    @patch("django.utils.timezone.now")
    def test_weekly_score_ok(self, mock_timezone):
        dt = timezone.datetime(2021, 1, 4, tzinfo=timezone.utc)
        mock_timezone.return_value = dt

        response = self.client.get(self.url)
        expected_response = [
            {
                "subreddit_id": self.weekly_score.subreddit.id,
                "redditor_id": self.weekly_score.redditor.id,
                "score_type": self.weekly_score.score_type,
                "score": str(self.weekly_score.score),
                "rank": self.weekly_score.rank,
                "week_number": self.weekly_score.week_number,
                "created_utc": self.weekly_score.created_utc.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

from decimal import Decimal

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from score import models, factories


class WeeklyRedditorScoreViewSetTest(TestCase):
    def setUp(self):
        self.weekly_score = factories.WeeklyRedditorScoreFactory(score_type="SUB")
        self.client = APIClient()
        # self.url = reverse("weekly-scores-list",  kwargs={'score_type': "SUB", 'week_number': 1 , 'year': 2021})

    def test_weekly_score_400(self):
        url = reverse("weekly-scores-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TODO: Update url config to use regex for filters
    # def test_weekly_score_ok(self):
    #     response = self.client.get(self.url)
    #     expected_response = [
    #         {
    #             "subreddit_id": self.weekly_score.subreddit.id,
    #             "redditor_id": self.weekly_score.redditor.id,
    #             "score_type": self.weekly_score.score_type,
    #             "score": Decimal('1000.10'), #TODO: self.weekly_score.score,
    #             "rank": self.weekly_score.rank,
    #             "week_number": self.weekly_score.week_number,
    #             "created_utc": "2021-01-04T00:00:00Z" #TODO: self.weekly_score.created_utc
    #         }
    #     ]
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

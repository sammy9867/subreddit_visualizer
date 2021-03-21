from django.urls import reverse
from django.test import TestCase
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

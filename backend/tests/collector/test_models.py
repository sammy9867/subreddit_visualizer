from django.test import TestCase
from reddit import models, factories


class SubredditTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.subreddit = factories.SubredditFactory()

    def test_fields(self):
        self.assertEqual(self.subreddit.id, "subreddit_id")
        self.assertEqual(self.subreddit.display_name, "subreddit_name")
        self.assertEqual(self.subreddit.title, "subreddit_title")

from django.test import TestCase
from reddit import models, factories
from decimal import Decimal


class SubredditTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.subreddit = factories.SubredditFactory()

    def test_fields(self):
        self.assertEqual(self.subreddit.id, "subreddit_id")
        self.assertEqual(self.subreddit.display_name, "subreddit_name")
        self.assertEqual(self.subreddit.title, "subreddit_title")


class WeeklyRedditorScoreTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.sub_score = factories.WeeklyRedditorScoreFactory(score_type="SUB")

    def test_fields(self):
        self.assertEqual(self.sub_score.subreddit.id, "subreddit_id")
        self.assertEqual(self.sub_score.redditor.id, "redditor_id")
        self.assertEqual(self.sub_score.score_type, "SUB")
        self.assertEqual(self.sub_score.score, Decimal("1000.10"))
        self.assertEqual(self.sub_score.rank, 1)
        self.assertEqual(self.sub_score.week_number, 1)

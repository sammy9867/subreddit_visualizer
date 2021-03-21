from decimal import Decimal, getcontext

from django.test import TestCase
from score import factories, serializers


class WeeklyRedditorScoreTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.weekly_score = factories.WeeklyRedditorScoreFactory.create()

    def test_contains_expected_fields(self):
        weekly_score_serializer = serializers.WeeklyRedditorScoreSerializer(
            self.weekly_score
        )
        actual_data = weekly_score_serializer.data
        self.assertEqual(
            set(actual_data.keys()),
            set(
                [
                    "subreddit_id",
                    "redditor_id",
                    "score_type",
                    "score",
                    "rank",
                    "week_number",
                    "created_utc",
                ]
            ),
        )

    # def test_fields(self):
    #     weekly_score_serializer = serializers.WeeklyRedditorScoreSerializer(
    #         [self.weekly_score], many=True
    #     )
    #     actual_data = weekly_score_serializer.data
    #     expected_data = [
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
    #     print(actual_data)
    #     print(expected_data)
    #     self.assertEqual(actual_data, expected_data)

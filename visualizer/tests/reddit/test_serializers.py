from django.test import TestCase
from reddit import factories, serializers


class SubredditSerializerTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.subreddit = factories.SubredditFactory()

    def test_contains_expected_fields(self):
        subreddit_serializer = serializers.SubredditSerializer(self.subreddit)
        actual_data = subreddit_serializer.data
        self.assertEqual(set(actual_data.keys()), set(["id", "display_name", "title"]))

    def test_fields(self):
        subreddit_serializer = serializers.SubredditSerializer(
            [self.subreddit], many=True
        )
        actual_data = subreddit_serializer.data
        expected_data = [
            {
                "id": self.subreddit.id,
                "display_name": self.subreddit.display_name,
                "title": self.subreddit.title,
            }
        ]
        self.assertEqual(actual_data, expected_data)

    def test_deserialize_data(self):
        data = {
            "id": "random_subreddit_id",
            "display_name": "Display Name",
            "title": "Title",
        }
        subreddit_serializer = serializers.SubredditSerializer(data=data)
        self.assertTrue(subreddit_serializer.is_valid())


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

    def test_fields(self):
        weekly_score_serializer = serializers.WeeklyRedditorScoreSerializer(
            [self.weekly_score], many=True
        )
        actual_data = weekly_score_serializer.data
        expected_data = [
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
        print(actual_data)
        print(expected_data)
        self.assertEqual(actual_data, expected_data)

    def test_deserialize_data(self):
        data = {
            "id": "random_subreddit_id",
            "display_name": "Display Name",
            "title": "Title",
        }
        subreddit_serializer = serializers.SubredditSerializer(data=data)
        self.assertTrue(subreddit_serializer.is_valid())

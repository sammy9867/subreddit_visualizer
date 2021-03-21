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

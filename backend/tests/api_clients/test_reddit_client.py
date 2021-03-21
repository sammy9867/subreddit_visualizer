from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from api_clients.reddit_client import RedditAPIClient
from reddit.models import Subreddit, Submission, Comment, Redditor


class RedditAPIClientTest(TestCase):
    def setUp(self):
        self.reddit_client = RedditAPIClient()
        self.submission_limit = 1
        self.comment_limit = 1
        self.end_day = datetime.now(tz=timezone.utc)
        self.start_day = self.end_day - timedelta(days=7)

    def test_get_subreddits(self):
        self.assertEqual(Subreddit.objects.count(), 0)
        self.assertEqual(Submission.objects.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(Redditor.objects.count(), 0)

        self.reddit_client.get_subreddits(
            ["news"],
            self.submission_limit,
            self.comment_limit,
            self.start_day.date(),
            self.end_day.date(),
        )

        self.assertEqual(Subreddit.objects.count(), 1)
        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertNotEqual(Redditor.objects.count(), 0)

    def test_validate_subreddit(self):
        subreddit = self.reddit_client.validate_subreddit("news")
        self.assertTrue(hasattr(subreddit, "id"))
        self.assertTrue(hasattr(subreddit, "display_name"))
        self.assertTrue(hasattr(subreddit, "title"))

    def test_save_subreddit(self):
        subreddit = self.reddit_client.validate_subreddit("news")
        self.assertEqual(Subreddit.objects.count(), 0)
        self.reddit_client.save_subreddit(subreddit)
        self.assertEqual(Subreddit.objects.count(), 1)

    def test_is_redditor_saved(self):
        subreddit = self.reddit_client.validate_subreddit("news")
        for sub in subreddit.top("week"):
            submission = sub
            break

        self.assertEqual(Redditor.objects.count(), 0)
        self.reddit_client.is_redditor_saved(submission.author)
        self.assertEqual(Redditor.objects.count(), 1)

    def test_is_submission_saved(self):
        subreddit = self.reddit_client.validate_subreddit("news")
        self.reddit_client.save_subreddit(subreddit)
        for sub in subreddit.top("week"):
            submission = sub
            break

        self.assertEqual(Submission.objects.count(), 0)
        self.reddit_client.is_submission_saved(
            submission, self.start_day.date(), self.end_day.date()
        )
        self.assertEqual(Submission.objects.count(), 1)

    def test_is_comment_saved(self):
        subreddit = self.reddit_client.validate_subreddit("news")
        self.reddit_client.save_subreddit(subreddit)
        for sub in subreddit.top("week"):
            sub.comments.replace_more(limit=1)
            submission = sub
            comment = sub.comments.list()[0]
            break
        self.reddit_client.is_submission_saved(
            submission, self.start_day.date(), self.end_day.date()
        )

        self.assertEqual(Comment.objects.count(), 0)
        self.reddit_client.is_comment_saved(
            comment, submission.id, self.start_day.date(), self.end_day.date()
        )
        self.assertEqual(Comment.objects.count(), 1)

    # def test_unix_timestamp_to_datetime(self):

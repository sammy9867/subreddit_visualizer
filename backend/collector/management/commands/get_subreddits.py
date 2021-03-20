from django.core.management.base import BaseCommand, CommandError
from api_clients.reddit import RedditAPIClient
from score.tasks import compute_score

from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Gets data from reddit to populate DB"

    def add_arguments(self, parser):
        parser.add_argument("submission_limit", type=int)
        parser.add_argument("comment_limit", type=int)

    def handle(self, *args, **options):
        submission_limit = options["submission_limit"]
        comment_limit = options["comment_limit"]
        end_day = datetime.now(tz=timezone.utc)
        start_day = end_day - timedelta(days=7)
        subreddits = ["Bitcoin", "wallstreetbets", "fitness"]
        reddit_client = RedditAPIClient()
        reddit_client.get_subreddits(
            subreddits,
            submission_limit,
            comment_limit,
            start_day.date(),
            end_day.date(),
        )

        for subreddit_name in subreddits:
            compute_score(subreddit_name, start_day, end_day, "SUB")
            compute_score(subreddit_name, start_day, end_day, "COM")

        self.stdout.write(self.style.SUCCESS("Successfully filled DB"))

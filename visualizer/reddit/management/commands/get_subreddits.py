from django.core.management.base import BaseCommand, CommandError
from api_clients.reddit_client import RedditAPIClient
from reddit.tasks import compute_score

from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class Command(BaseCommand):
    help = "Gets data from reddit to populate DB"

    def add_arguments(self, parser):
        parser.add_argument("submission_limit", type=int)
        parser.add_argument("comment_limit", type=int)

    def handle(self, *args, **options):
        submission_limit = options["submission_limit"]
        comment_limit = options["comment_limit"]
        end_day = timezone.now()
        start_day = end_day - timedelta(days=7)
        reddit_client = RedditAPIClient()
        subreddits = settings.SUBREDDIT_LIST
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
